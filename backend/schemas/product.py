from pydantic import BaseModel

class ProductCreate(BaseModel):
    business_id:int

    name:str
    price:float
    stock:int

class ProductResponse(ProductCreate):
    id:int

    class Config:
        from_attributes = True