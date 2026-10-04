from pydantic import BaseModel, EmailStr
from typing import Optional

# Admin Schemas
class AdminRegister(BaseModel):
    name:str
    email:EmailStr
    password:str
    business_name:str

class AdminLogin(BaseModel):
    identifier:str #Can be email or admin_code
    password:str

class AdminRegisterResponse(BaseModel):
    message:str = "Admin registered successfully! Save your unique Admin ID."
    admin_code:str
    email:str
    name:str
    access_token:str
    token_type:str ="bearer"

# Customer Schemas
class CustomerRegister(BaseModel):
    name:str
    email:EmailStr
    password:str
    phone:Optional[str]=None

class CustomerLogin(BaseModel):
    email:EmailStr
    password:str

# Token Response
class TokenResponse(BaseModel):
    access_token:str
    token_type:str = "bearer"
    user_type:str #customer or admin