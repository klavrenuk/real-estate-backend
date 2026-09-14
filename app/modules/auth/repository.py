from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.model import User


async def create_user(db: AsyncSession, name: str) -> User:
    user = User(name=name)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user_by_name(db: AsyncSession, name: str) -> User | None:
    result = await db.execute(select(User).where(User.name == name))
    return result.scalar_one_or_none()