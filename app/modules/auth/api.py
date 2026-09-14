from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.auth.schemas import UserCreate, UserOut
from app.modules.auth.service import create_user_if_not_exists

router = APIRouter(prefix="/auth", tags=["auth"])

DbSession = Annotated[AsyncSession, Depends(get_db)]


@router.get("/me")
async def me() -> dict[str, str]:
    return {"message": "все ок"}


@router.post("/create-user", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, db: DbSession) -> UserOut:
    user = await create_user_if_not_exists(db, payload.name)
    return UserOut.model_validate(user)