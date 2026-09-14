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
│   └── auth/           # регистрация, логин, токены
│       └── api.py / service.py / repository.py / schemas.py
└── main.py             # FastAPI-приложение
```

Архитектура — модульный монолит (feature-first): деление по доменам, внутри каждого модуля слои api → service → repository. Модули общаются через сервисный слой, общий `core/` переиспользуют все.

## Установка

```bash
uv sync          # создать .venv и установить зависимости
cp .env.example .env   # и вписать реальные DATABASE_URL и SECRET_KEY
uv run uvicorn app.main:app --reload  # run to dev mode

```

## Проверка

- OpenAPI-документация: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

## Линт и тесты

```bash
uv run ruff check .
uv run pytest
```