from pydantic import BaseModel

class OrderCheckoutRequest(BaseModel):
    customer_id:int
    product_name:str
    discount_percent: float = 0

class OrderCheckoutResponse(BaseModel):
    order_id:int
    customer_id:int
    product_name:str
    original_price:float
    discount_percent:float
    final_price:float
    status:str