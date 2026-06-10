from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.dependencies import get_db
from models.business import Business
from models.policy import Policy
from schemas.policy import(
    PolicyCreate,
    PolicyResponse
)
router = APIRouter(
    prefix="/policies",
    tags =["Policies"]
)
@router.post("/",response_model=PolicyResponse)
def create_policy(
    policy:PolicyCreate,
    db:Session = Depends(get_db)
):
    #checking if business exist
    business = (
        db.query(Business)
        .filter(Business.id == policy.business_id)
        .first()
    )
    if business is None:
        raise HTTPException(
            status_code=404,
            detail=f"Business with ID {policy.business_id} does not exist"
        )
    
    #checking if policy already exists
    existing_policy = (
        db.query(Policy)
        .filter(Policy.business_id == policy.business_id)
        .first()
    )
    if existing_policy:
        raise HTTPException(
            status_code=409,
            detail="A policy already exists for this business"
        )


    new_policy =Policy(**policy.model_dump())
    db.add(new_policy)
    db.commit()
    db.refresh(new_policy)

    return new_policy

@router.get("/",response_model=list[PolicyResponse])
def get_policies(
    db:Session = Depends(get_db)
):
    return db.query(Policy).all()

@router.get("/{policy_id}",response_model=PolicyResponse)
def get_policy(
    policy_id:int,
    db:Session=Depends(get_db)
):
    policy = db.query(Policy).filter(
        Policy.id == policy_id
    ).first()

    if policy is None:
        raise HTTPException(
            status_code=404,
            detail=f"Policy with ID {policy_id} not found"
        )
    return policy