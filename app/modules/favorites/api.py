from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.core.database import get_db

from app.modules.favorites.schemas import FavoriteOut, FavoriteCreate
from app.modules.favorites.service import get_by_user, create_favorite

router = APIRouter(prefix='/favorites')

DbSession = Annotated[AsyncSession, Depends(get_db)]


@router.get('/by-user', response_model=list[FavoriteOut])
async def api_get_favorites_list_by_users(db: DbSession) -> list[FavoriteOut]:
    return await get_by_user(db)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def api_create_favorite(payload: FavoriteCreate, db: DbSession) -> bool:
    return await create_favorite(db, payload.user_id, payload.listing_id)
