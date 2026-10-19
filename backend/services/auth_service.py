import os 
import jwt
import bcrypt
from datetime import datetime,timedelta, timezone
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database.dependencies import get_db
from models.admin import Admin
from models.customer import Customer

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError(
        "JWT_SECRET_KEY environment variable is not configured"
    )
ALGORITHM ="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24 #24 HRS

security = HTTPBearer()

def hash_password(password:str) -> str:
    pwd_bytes = password.encode('utf-8')[:72]
    salts = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes,salts).decode('utf-8')

def verify_password(plain_password:str,hashed_password:str)-> bool:
    pwd_bytes = plain_password.encode('utf-8')[:72]
    return bcrypt.checkpw(pwd_bytes,hashed_password.encode('utf-8'))

def create_access_token(data:dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire, "sub":str(data["sub"])})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def get_current_admin(
        credentials:HTTPAuthorizationCredentials = Depends(security),
        db:Session = Depends(get_db)
) -> Admin:
    token = credentials.credentials
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        if payload.get("user_type") != "admin":
            raise HTTPException(status_code=403, detail="Admin access required")

        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(status_code=401,detail="Invalid token: missing subject")
        admin_id  = int(sub)

    except jwt.PyJWTError as e:
        print(f"JWT Verification Failed: {type(e).__name__} ({str(e)})")
        raise HTTPException(status_code=401,detail=f"Invalid token: {type(e).__name__} ({str(e)})")

    admin = db.query(Admin).filter(Admin.id==admin_id).first()

    if not admin:
        raise HTTPException(status_code=404,detail="Admin account not found in database")
    return admin

def get_current_customer(
        credentials:HTTPAuthorizationCredentials = Depends(security),
        db:Session = Depends(get_db)
) -> Customer:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("user_type") != "customer":
            raise HTTPException(status_code=403,detail="Customer access required")

        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(status_code=403, detail="Invalid token: missing subject")
        customer_id = int(sub)

    except jwt.PyJWTError as e:
        print(f"Customer JWT Verification Failed: {type(e).__name__} ({str(e)})")
        raise HTTPException(status_code=401, detail=f"Invalid token: {type(e).__name__} ({str(e)})")

    customer =  db.query(Customer).filter(Customer.id==customer_id).first()

    if not customer:
        raise HTTPException(status_code=404,detail="Customer not found")
    
    return customer