from datetime import datetime

from app.core.database import Base
from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Favorite(Base):
    __tablename__ = 'favorites'

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True
    )
    listing_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('listings.id', ondelete='CASCADE'), index=True, primary_key=True
    )

    listing = relationship('Listing', passive_deletes=True)
