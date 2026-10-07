from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.favorites.model import Favorite


async def get_by_user(db: AsyncSession, user_id: int) -> list[Favorite]:
    result = await db.execute(
        select(Favorite)
        .where(Favorite.user_id == user_id)
    )

    return result.scalars().all()


async def create(db: AsyncSession, user_id: int, listing_id: int) -> Favorite:
    favorite = Favorite(user_id=user_id, listing_id=listing_id)
    db.add(favorite)

    await db.flush()
    return favorite


async def get_by_user_and_listing(db: AsyncSession, user_id: int, listing_id: int) -> Favorite | None:
    favorite = await db.execute(
        select(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.listing_id == listing_id
        )
    )

    return favorite.scalar_one_or_none()


async def delete(db: AsyncSession, favorite: Favorite):
    result = await db.execute(
        delete(Favorite).where(
            Favorite.user_id == favorite.user_id,
            Favorite.listing_id == favorite.listing_id,
        )
    )

    await db.flush()
    return result.rowcount > 0
