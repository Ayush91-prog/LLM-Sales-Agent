from pydantic import BaseModel
from datetime import datetime

class OrderCreate(BaseModel):
    business_id:int
    customer_id:int
    total_amount:float

class OrderStatusUpdate(BaseModel):
    status:str
    
class OrderResponse(OrderCreate,OrderStatusUpdate):
    id:int
    customer_name:str
    created_at:datetime

    class Config:
        from_attributes=True