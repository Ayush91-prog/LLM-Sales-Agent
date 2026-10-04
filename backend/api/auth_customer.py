from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.dependencies import get_db
from models.customer import Customer
from schemas.auth import CustomerRegister, CustomerLogin, TokenResponse
from services.auth_service import hash_password,verify_password,create_access_token,get_current_customer

router = APIRouter(
    prefix="/auth/customer",
    tags=["Customer Auth"]
)

@router.post("/register",response_model=TokenResponse)
def register_customer(data:CustomerRegister, db: Session  = Depends(get_db)):
    existing = db.query(Customer).filter(Customer.email==data.email).first()

    if existing:
        raise HTTPException(status_code=400,detail="Email already registered")

    new_customer = Customer(
        name=data.name,
        email=data.email,
        phone=data.phone,
        hashed_password=hash_password(data.password),
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    token = create_access_token({"sub":new_customer.id, "user_type":"customer"})
    return TokenResponse(access_token=token, user_type="customer")

@router.post("/login",response_model=TokenResponse)
def login_customer(data:CustomerLogin,db:Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.email==data.email).first()

    if not customer or not customer.hashed_password or not verify_password(data.password,customer.hashed_password):
        raise HTTPException(status_code=401,detail="Invalid Email or Password")

    token = create_access_token({"sub":customer.id, "user_type":"customer"})
    return TokenResponse(
        access_token=token,
        user_type="customer"
    )

@router.get("/me")
def get_customer_profile(current_customer:Customer = Depends(get_current_customer)):
    return {
        "id":current_customer.id,
        "name":current_customer.name,
        "email":current_customer.email,
        "phone":current_customer.phone
    }