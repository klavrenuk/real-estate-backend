from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.listings.model import Listing
from app.modules.listings.schemas import ListingCreate

async def create_listening(db:AsyncSession, payload:ListingCreate) -> ListingCreate:
    listing = Listing(payload.model_dump())
    db.add()

    await db.commit()
    await db.refresh(listing)
    return listing


async def get_all(db:AsyncSession) -> list[Listing]:
    return await db.query(Listing).all()