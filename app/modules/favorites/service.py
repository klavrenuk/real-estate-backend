from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.modules.favorites import repository
from app.modules.favorites.schemas import FavoriteOut


async def get_by_user(db: AsyncSession, user_id: int) -> FavoriteOut:
    return await repository.get_by_user(db, user_id)


async def create_favorite(db: AsyncSession, user_id: int, listing_id: int) -> bool:
    try:
        await repository.create(db, user_id, listing_id)
        return True
    except IntegrityError:
        await db.rollback()
        return False
