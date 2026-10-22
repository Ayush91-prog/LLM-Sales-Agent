from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import Integer, String, ForeignKey, DateTime
from datetime import datetime, UTC
from database.base import Base 

class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key = True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    phone: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    address: Mapped[str | None] = mapped_column(
        String,
        nullable = True
    )

    hashed_password:Mapped[str | None] = mapped_column(
        String, 
        nullable=True
        )
    
    created_at:Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC)
        )