from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float,ForeignKey

from database.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    business_id: Mapped[int] = mapped_column(
        ForeignKey("businesses.id"),
        nullable=False
        )
    name: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)