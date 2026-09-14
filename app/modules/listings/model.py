from app.core.database import Base

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

class Listing(Base):
    __tablename__ = 'listings'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    price: Mapped[int] = mapped_column()
    phone: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)