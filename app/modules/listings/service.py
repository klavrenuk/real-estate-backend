from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.listings import repository
from app.modules.listings.model import Listing
from app.modules.listings.schemas import ListingCreate


async def create_listing(db: AsyncSession, payload: ListingCreate) -> Listing:
    return await repository.create_listing(db, payload)


async def get_listings(db: AsyncSession) -> list[Listing]:
    return await repository.get_all(db)