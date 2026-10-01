# real-estate-backend

Backend сервиса недвижимости на Python (FastAPI, PostgreSQL).

## Стек

- Python 3.13+, FastAPI, Uvicorn
- SQLAlchemy 2 (async) + asyncpg
- Alembic (миграции), pydantic-settings
- JWT (PyJWT) + bcrypt

## Структура

```
app/
├── core/               # общий слой: конфиг, БД-сессия, безопасность (JWT, хеши)
├── modules/
│   └── auth/           # модуль авторизации
│       ├── api.py          # HTTP-слой (роутеры FastAPI)
│       ├── service.py      # бизнес-логика
│       ├── repository.py   # доступ к данным (SQL-запросы)
│       ├── model.py        # SQLAlchemy-модель (таблица users)
│       └── schemas.py      # Pydantic-схемы (контракты данных)
└── main.py             # FastAPI-приложение, lifespan, подключение роутеров

alembic.ini             # конфиг Alembic (URL берётся из .env, см. migrations/env.py)
migrations/
├── env.py              # async-конфигурация, автоимпорт всех app/modules/*/model.py
└── versions/           # сами миграции
```

Архитектура — модульный монолит (feature-first): деление по доменам, внутри каждого модуля слои. Модули общаются через сервисный слой, общий `core/` переиспользуют все.

## Архитектура модулей

### `schemas.py` — Контракты данных (Pydantic-модели)

Описывает форму входящих/исходящих JSON:
- `UserCreate` — что принимаем в body при создании пользователя (поле `name: str`).
- `UserOut` — что отдаём клиенту (`id`, `name`), определяет вид ответа и автоматически генерирует JSON-схему для Swagger.
- Не содержит логики — только структура данных и валидация.

### `repository.py` — Доступ к данным (SQL-запросы)

Низкоуровневая работа с таблицей через SQLAlchemy async:
- `create_user(db, name)` — создаёт объект `User`, коммитит, возвращает.
- `get_user_by_name(db, name)` — `SELECT ... WHERE name = ?`, возвращает объект или `None`.
- Не знает HTTP и бизнес-правил — только запросы.

### `service.py` — Бизнес-логика

Сидит между API и репозиторием, применяет правила:
- `create_user_if_not_exists(db, name)` — сначала проверяет через репозиторий, нет ли уже такого имени; если есть — выбрасывает `HTTPException(409)`, иначе создаёт.
- Логика вынесена сюда, а не в `api.py`, чтобы её можно было переиспользовать в другом роутере или скрипте без импорта фреймворка.

### `api.py` — HTTP-слой (роутер FastAPI)

Один файл — один роутер, привязанный к URL-префиксу `/auth`:
- `GET /me` — тривиальный эндпоинт, возвращает сообщение.
- `POST /create-user` — принимает `UserCreate` через `Depends`, вызывает `service.create_user_if_not_exists`, возвращает `UserOut`.
- Не содержит логики проверок — только вызов сервиса и формирование HTTP-ответа.

### Поток вызова

```
api.py (роутер)
  → service.py (бизнес-правило)
    → repository.py (SQL)
      → model.py (таблица)
        → PostgreSQL
```

### `core/` — Общая инфраструктура

| Файл | Зачем |
|---|---|
| `config.py` | `Settings` через pydantic-settings: DATABASE_URL, SECRET_KEY, PORT и пр. Читает `.env` |
| `database.py` | async engine (asyncpg), сессия, базовый `Base` для моделей, зависимость `get_db` |
| `security.py` | Хеширование паролей (bcrypt), создание/проверка JWT-токенов (PyJWT) |

## Установка

```bash
uv sync                       # создать .venv и установить зависимости
cp .env.example .env          # вписать реальные DATABASE_URL и SECRET_KEY
alembic upgrade head          # применить миграции к БД
uv run dev                    # запуск в dev-режиме (порт берётся из .env)
```

## Миграции (Alembic)

Схема БД управляется только Alembic. Приложение **не** создаёт таблицы само
(в `lifespan` нет `create_all`), поэтому после клона нужно один раз прогнать миграции.

URL для миграций берётся из `app.core.config` → `.env`, в `alembic.ini` он пустой намеренно:
иначе миграции могли бы пойти в одну БД, а приложение — в другую.

```bash
alembic upgrade head          # применить миграции
alembic downgrade -1          # откатить последнюю
alembic current               # на какой ревизии сейчас БД
alembic history               # список миграций
alembic revision --autogenerate -m "add users table"   # создать миграцию
alembic check                 # есть ли расхождения между моделями и БД
```

Рабочий цикл: изменил модель → `alembic revision --autogenerate -m "..."` →
посмотри глазами сгенерированный файл в `migrations/versions/` →
`alembic upgrade head`.

`migrations/env.py` сам импортирует все `app/modules/*/model.py`, поэтому новая модель
подхватывается автогенерацией автоматически. Учти: для этого каждая папка модуля
должна содержать `__init__.py`, иначе пакет не будет найден.

> `alembic revision --autogenerate` сравнивает модели с **текущей** БД. Если таблицы
> ещё не создавались, диф будет пустым — сначала сделай `alembic upgrade head` на чистой базе.

## Проверка

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health: http://127.0.0.1:8000/health

Порт по умолчанию `8000` (`Settings.port`). Чтобы сменить — добавь `PORT=8002` в `.env`.

## Линт и тесты

```bash
uv run ruff check .
uv run pytest
```