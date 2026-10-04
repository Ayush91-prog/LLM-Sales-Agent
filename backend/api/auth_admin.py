from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.dependencies import get_db
from models.admin import Admin, generate_admin_code
from models.business import Business
from schemas.auth import AdminRegister, AdminLogin, AdminRegisterResponse,TokenResponse
from services.auth_service import hash_password,verify_password,create_access_token,get_current_admin

router = APIRouter(prefix="/auth/admin", tags=["Admin Auth"])

@router.post("/register", response_model=AdminRegisterResponse)
def register_admin(data:AdminRegister, db:Session = Depends(get_db)):
    existing = db.query(Admin).filter(Admin.email== data.email).first()
    if existing:
        raise HTTPException(status_code=400,detail="Email already registered")

    # Automatically create new Business
    new_business = Business(name=data.business_name, email=data.email)
    db.add(new_business)
    db.commit()
    db.refresh(new_business)

    # Created admin linked to new Business
    code = generate_admin_code()
    new_admin = Admin(
        admin_code=code,
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
        business_id=new_business.id
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    token = create_access_token({"sub":new_admin.id, "user_type":"admin", "business_id":new_business.id})
    return AdminRegisterResponse(
        admin_code=code,
        email=new_admin.email,
        name=new_admin.name,
        access_token=token
)

@router.post("/login", response_model=TokenResponse)
def login_admin(data:AdminLogin, db:Session = Depends(get_db)):
    admin= db.query(Admin).filter(
        (Admin.email==data.identifier) | (Admin.admin_code==data.identifier)
    ).first()

    if not admin or not verify_password(data.password,admin.hashed_password):
        raise HTTPException(status_code=401,details="Invalid Admin Code / Email or Password")

    token = create_access_token({"sub":admin.id, "user_type":"admin" , "business_id":admin.business_id})
    return TokenResponse(access_token=token, user_type="admin")

@router.get("/me")
def get_admin_profile(current_admin:Admin = Depends(get_current_admin)):
    return{
        "id":current_admin.id,
        "name":current_admin.name,
        "email":current_admin.email,
        "admin_code":current_admin.admin_code,
        "business_id":current_admin.business_id
    }