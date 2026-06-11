from pydantic import BaseModel

class CustomerCreate(BaseModel):
    business_id: int

    name: str
    email: str
    phone: str | None=None

class CustomerResponse(CustomerCreate):
    id:int
    
    class Config:
        from_attributes = True