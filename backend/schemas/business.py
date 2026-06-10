from pydantic import BaseModel

class BusinessCreate(BaseModel):
    name:str
    email:str | None=None
    phone:str | None=None
    currency:str | None="INR"
    brand_voice:str | None=None

class BusinessResponse(BusinessCreate):
    id:int

    class Config:
        from_attributes = True 