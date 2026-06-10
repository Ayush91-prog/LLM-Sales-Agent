from sqlalchemy import (Column, Integer, Float, Boolean,Text, ForeignKey)
from database.base import Base

class Policy(Base):
    __tablename__ = "policies"

    id=Column(Integer,primary_key=True,index=True)

    business_id = Column(Integer, ForeignKey("businesses.id"),nullable=False, unique=True)
    max_discount_percent=Column(Float,nullable=True)
    min_order_value_for_discount=Column(Float,nullable=True)
    
    allow_bulk_purchase = Column(Boolean, default=False)
    allow_first_time_customer = Column(Boolean, default=False)
    allow_seasonal_sale = Column(Boolean, default=False)
    allow_loyalty_reward = Column(Boolean, default=False)
    allow_price_match = Column(Boolean, default=False)
    allow_custom_reason = Column(Boolean, default=False)

    free_shipping_over = Column(Float,nullable=True)
    flat_shipping_fee = Column(Float, nullable=True)

    return_window_days  = Column(Integer,nullable=True)
    non_refundable_categories =Column(Text,nullable=True)