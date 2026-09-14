from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.listings.repository import create_listening, get_all

from app.modules.listings.model import Listing

from app.modules.listings.schemas import ListingCreate

async def crate_listing(db:AsyncSession, payload:ListingCreate) -> Listing:
    return await create_listening(db, payload)

async def get_listings(db:AsyncSession) -> list[Listing]:
    return await get_all(db)