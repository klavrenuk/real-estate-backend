from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.model import User
from app.modules.auth.repository import create_user, get_user_by_name


async def create_user_if_not_exists(db: AsyncSession, name: str) -> User:
    existing = await get_user_by_name(db, name)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this name already exists",
        )
    return await create_user(db, name)