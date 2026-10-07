from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.modules.favorites import repository
from app.modules.favorites.schemas import FavoriteOut

from app.modules.favorites.exceptions import FavoriteAlreadyExistsError, ListingNotFoundError


async def get_by_user(db: AsyncSession, user_id: int) -> list[FavoriteOut]:
    return await repository.get_by_user(db, user_id)


async def create_favorite(db: AsyncSession, user_id: int, listing_id: int) -> bool:
    if await repository.get_by_user_and_listing(db, user_id, listing_id):
        return FavoriteAlreadyExistsError

    if await listing_repository.get(db, listing_id) is None:
        raise ListingNotFoundError(listing_id)

    try:
        await repository.create(db, user_id, listing_id)
        return True
    except IntegrityError:
        await db.rollback()
        return False


async def delete_favorite_from_user(db: AsyncSession, user_id: int, listing_id: int) -> bool:
    deleted = await repository.get_by_user_and_listing(db, user_id, listing_id)
    db.commit()
    return deleted
