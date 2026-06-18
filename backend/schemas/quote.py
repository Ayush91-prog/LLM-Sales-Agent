from pydantic import BaseModel

class QuoteRequest(BaseModel):
    product_name:str

class QuoteResponse(BaseModel):
    product_name: str
    price: float
    shipping_fee: float
    discount_available:bool
    max_discount_percent:float | None
    estimated_total: float
    