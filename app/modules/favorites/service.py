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


async def delete_favorite_from_user(db: AsyncSession, user_id: int, listing_id: int) -> bool:
    favorite = await repository.get_by_user_and_listing(db, user_id, listing_id)

    if favorite is None:
        return True

    await repository.delete(db, favorite)
    return True
