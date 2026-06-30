from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer,Float, String, ForeignKey, DateTime
from datetime import datetime,UTC

from database.base import Base

class Order(Base):
    __tablename__ = "orders"

    id:Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
    business_id:Mapped[int] = mapped_column(
        ForeignKey("businesses.id"),
        nullable=False
    )
    customer_id:Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False
    )
    product_id:Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False
    )
    total_amount:Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    status:Mapped[str] = mapped_column(
        String,
        default="pending"
    )
    customer = relationship("Customer")
    product = relationship("Product")
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC)
    )
