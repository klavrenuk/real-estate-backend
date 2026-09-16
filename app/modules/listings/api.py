from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.modules.listings.service import get_listings, create_listing 
from app.modules.listings.schemas import ListingCreate, ListingOut

router = APIRouter(prefix='/listings')

DbSession = Annotated[AsyncSession, Depends(get_db)]

@router.get('/', response_model=list[ListingOut])
async def list_listings(db: DbSession) -> list[ListingOut]:
    listings = await get_listings(db)
    return listings



@router.get('/{id}')
async def get_listing(id:int, db: DbSession) -> ListingOut:
    return {

    }

@router.post('/')
async def create_listings(payload:ListingCreate, db: DbSession) -> ListingOut:
    new_listening = create_listing (db, payload)
    return {
        'listening': new_listening
    }

@router.patch('/{id}')
async def update_listing(id:int, db:DbSession) -> ListingOut:
    return {}