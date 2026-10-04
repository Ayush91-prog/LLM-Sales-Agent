from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.dependencies import get_db
from models.business import Business
from models.policy import Policy
from models.admin import Admin
from services.auth_service import get_current_admin
from schemas.policy import(
    PolicyCreate,
    PolicyResponse
)

router = APIRouter(
    prefix="/policies",
    tags =["Policies"]
)
@router.post("/",response_model=PolicyResponse)
def create_or_update_policy(
    policy_data:PolicyCreate,
    db:Session = Depends(get_db),
    current_admin:Admin = Depends(get_current_admin)
):
    
    target_business_id = current_admin.business_id

    if not target_business_id :
        raise HTTPException(
            status_code=400,
            detail="Admin is not associated with any business"
        )
    
    #checking if policy already exists
    existing_policy = (
        db.query(Policy)
        .filter(Policy.business_id == target_business_id)
        .first()
    )
    if existing_policy:
        for key,value in policy_data.model_dump().items():
            if key != "business_id" and value is not None:
                setattr(existing_policy,key,value)
        db.commit()
        db.refresh(existing_policy)
        return existing_policy


    new_policy =Policy(**policy_data.model_dump())
    new_policy.business_id = target_business_id
    db.add(new_policy)
    db.commit()
    db.refresh(new_policy)

    return new_policy

@router.get("/my",response_model=PolicyResponse)
def get_my_store_policy(
    db:Session = Depends(get_db),
    current_admin:Admin = Depends(get_current_admin)
):
    if not current_admin.business_id:
        raise HTTPException(
            status_code=400,
            detail="Admin is not associated with any business"
        )

    policy = db.query(Policy).filter(Policy.business_id==current_admin.business_id).first()
    if not policy:
        raise HTTPException(
            status_code=404,
            detail="No policy found for your business"
        )
    return policy