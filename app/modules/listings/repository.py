from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.listings.model import Listing
from app.modules.listings.schemas import ListingCreate

async def create_listing (db:AsyncSession, payload:ListingCreate) -> ListingCreate:
    listing = Listing(**payload.model_dump())  # распаковка dict в именованные аргументы Listing
    db.add(listing)

    await db.commit()
    await db.refresh(listing)
    return listing


async def get_all(db:AsyncSession) -> list[Listing]:
    items = await db.execute(select(Listing).order_by(Listing.id.desc()))
    return items.scalars().all()