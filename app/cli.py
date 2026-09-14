import uvicorn

from app.core.config import get_settings


def dev() -> None:
    settings = get_settings()
    uvicorn.run("app.main:app", host="127.0.0.1", port=settings.port, reload=True)