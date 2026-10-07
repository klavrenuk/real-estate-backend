from pydantic import BaseModel, Field, ConfigDict


class FavoriteOut(BaseModel):
    model_config = ConfigDict(from_attribute=True)

    user_id: int
    listing_id: int


class FavoriteDelete(BaseModel):
    user_id: int
    listing_id: int


class FavoriteCreate(BaseModel):
    user_id: int
    listing_id: int
