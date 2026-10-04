from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, DateTime
from datetime import datetime
import secrets
from database.base import Base

def generate_admin_code() -> str:
    """Generates a unique code like ADM-7A9B2C"""
    return f"ADM-{secrets.token_hex(3).upper()}"

class Admin(Base):
    __tablename__="admins"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    admin_code:Mapped[str] = mapped_column(String, unique=True, index=True, default=generate_admin_code)
    business_id:Mapped[int|None] = mapped_column(ForeignKey("businesses.id"), nullable=True)
    name:Mapped[str] = mapped_column(String, nullable=False)
    email:Mapped[str] = mapped_column(String,unique=True, index=True, nullable=False)
    hashed_password:Mapped[str] = mapped_column(String, nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)