from pydantic import BaseModel, Field, ConfigDict


class FavoriteOut(BaseModel):
    user_id: int
    listing_id: int


class FavoriteDelete(BaseModel):
    user_id: int
    listing_id: int


class FavoriteCreate(BaseModel):
    user_id: int
    listing_id: int

    model_config = ConfigDict(from_attribute=True)
