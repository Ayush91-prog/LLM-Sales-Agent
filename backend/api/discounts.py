from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.dependencies import get_db

from schemas.discount import (DiscountRequest,DiscountResponse)
from services.product_service import search_products
from services.policy_service import get_policy
from services.discount_service import apply_discount

router=APIRouter(
    prefix="/discounts",
    tags=["Discounts"]
)

@router.post("/apply",response_model=DiscountResponse)
def apply_discount_api(
    request:DiscountRequest,
    db:Session = Depends(get_db)
):
    products = search_products(
        db,
        request.product_name
    )

    if not products:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    
    product = products[0]
    policy = get_policy(db)
    return apply_discount(
        product,
        policy,
        request.discount_percent
    )