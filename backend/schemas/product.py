from pydantic import BaseModel, ConfigDict
from typing import Optional

class ProductCreate(BaseModel):
    name:str
    price:float
    stock:int
    business_id:Optional[int] = None

class ProductResponse(ProductCreate):
    id:int
    business_id: int
    model_config= ConfigDict(from_attributes = True)