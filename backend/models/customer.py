from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import Integer, String, ForeignKey

from database.base import Base 

class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key = True,
        index=True
    )

    business_id: Mapped[int] = mapped_column(
        ForeignKey("businesses.id"),
        nullable=False
    )

    name: Mapped[int] = mapped_column(
        String,
        nullable=False
    )

    email: Mapped[int] = mapped_column(
        String,
        nullable=False
    )
    phone: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )