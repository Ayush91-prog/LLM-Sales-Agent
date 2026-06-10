from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.dependencies import get_db
from models.business import Business
from schemas.business import (BusinessCreate,BusinessResponse)

router=APIRouter(
    prefix="/business",
    tags=["Business"]
)

#Create Business
@router.post("/",response_model=BusinessResponse)
def create_business(
    business:BusinessCreate,
    db:Session = Depends(get_db)
):
    new_business= Business(**business.model_dump())

    db.add(new_business)
    db.commit()
    db.refresh(new_business)
    
    return new_business

#Get all business
@router.get("/",response_model=list[BusinessResponse])
def get_business(
    db:Session = Depends(get_db)
):
    return db.query(Business).all()