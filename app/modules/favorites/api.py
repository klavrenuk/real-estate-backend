from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.core.database import get_db

from app.modules.favorites.schemas import FavoriteOut, FavoriteCreate, FavoriteDelete
from app.modules.favorites.service import get_by_user, create_favorite, delete_favorite_from_user

from app.modules.favorites.exceptions import FavoriteAlreadyExistsError, ListingNotFoundError

router = APIRouter(prefix='/favorites')

DbSession = Annotated[AsyncSession, Depends(get_db)]


@router.get('/by-user', response_model=list[FavoriteOut])
async def api_get_favorites_list_by_users(db: DbSession, user_id: int) -> list[FavoriteOut]:
    return await get_by_user(db, user_id)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def api_create_favorite(db: DbSession, payload: FavoriteCreate) -> bool:
    try:
        favorite = await create_favorite(db, payload.user_id, payload.listing_id)
    except FavoriteAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ListingNotFoundError:
        raise HTTPExeption(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    
    return favorite


@router.delete('/', status_code=status.HTTP_200_OK)
async def api_delete_favorite_from_user(db: DbSession, payload: FavoriteDelete) -> bool:
    return await delete_favorite_from_user(db, payload.user_id, payload.listing_id)
