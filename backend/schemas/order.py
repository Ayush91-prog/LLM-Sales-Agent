from pydantic import BaseModel
from datetime import datetime

class OrderCreate(BaseModel):
    business_id:int
    customer_id:int

    total_amount:float


class OrderResponse(OrderCreate):
    id:int
    status:str
    created_at:datetime

    class Config:
        from_attributes=True