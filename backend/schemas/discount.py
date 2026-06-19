from pydantic import BaseModel

class DiscountRequest(BaseModel):
    product_name:str
    discount_percent:float

class DiscountResponse(BaseModel):
    product_name:str
    original_price: float
    discount_percent:float
    discount_amount: float
    final_price:float