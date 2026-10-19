from pydantic import BaseModel, ConfigDict

class CustomerCreate(BaseModel):
    name: str
    email: str
    phone: str | None=None

class CustomerResponse(CustomerCreate):
    id:int
    model_config = ConfigDict(from_attributes=True)