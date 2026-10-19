from pydantic import BaseModel, ConfigDict

class BusinessCreate(BaseModel):
    name:str
    email:str | None=None
    phone:str | None=None
    currency:str | None="INR"
    brand_voice:str | None=None

class BusinessResponse(BusinessCreate):
    id:int
    model_config = ConfigDict(from_attributes = True )