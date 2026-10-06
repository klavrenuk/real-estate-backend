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

    await db.commit()
    await db.refresh(favorite)
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
    await db.delete(favorite)
    await db.commit()
