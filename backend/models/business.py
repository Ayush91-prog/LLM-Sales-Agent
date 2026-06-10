from sqlalchemy import Column, Integer, String, Text
from database.base import Base

class Business(Base):
    __tablename__="businesses"

    id = Column(Integer,primary_key=True, index=True)

    name = Column(String,nullable=False)
    email = Column(String,nullable=True)
    phone = Column(String,nullable=True)
    currency = Column(String,nullable=True,default="INR")
    brand_voice =Column(Text,nullable=True)
