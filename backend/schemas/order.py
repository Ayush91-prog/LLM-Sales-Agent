from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum

class OrderStatus(str,Enum):
    pending = "pending"
    paid = "paid"
    processing = "processing"
    shipped = "shipped"
    delivered ="delivered"
    cancelled = "cancelled"

class OrderCreate(BaseModel):
    business_id:int
    customer_id:int
    product_id:int
    total_amount:float

class OrderStatusUpdate(BaseModel):
    status:OrderStatus
    
class OrderResponse(OrderCreate):
    id:int
    customer_name:str
    status:OrderStatus
    created_at:datetime
    model_config = ConfigDict(from_attributes=True)