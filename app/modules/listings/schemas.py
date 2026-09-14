from pydantic import BaseModel, Field, ConfigDict

class ListingCreate(BaseModel):
    name: str = Field(min_length=3, max_length=255)
    price: int = Field(gt=0)
    phone: str = Field(min_length=5, max_length=255),
    description: str = Field()


class ListingOut(BaseModel):
    id: int
    name: str
    price: int
    phone: str
    description: str

    model_config = ConfigDict(from_attributes=True)