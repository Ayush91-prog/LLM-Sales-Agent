from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.dependencies import get_db
from services.analytics_service import get_sales_report

router=APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.get("/business/{business_id}")
def business_sales_report(
    business_id:int,
    db:Session = Depends(get_db)
):
    return get_sales_report(
        db,
        business_id
    )