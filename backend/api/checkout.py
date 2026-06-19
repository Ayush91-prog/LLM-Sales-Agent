from fastapi import (APIRouter,Depends,HTTPException)
from sqlalchemy.orm import Session
from database.dependencies import get_db
from schemas.order_checkout import(OrderCheckoutRequest,OrderCheckoutResponse)
from services.product_service import search_products
from services.policy_service import get_policy
from services.checkout_service import create_checkout_order

router=APIRouter(
    prefix="/checkout",
    tags=["Checkout"]
)

@router.post(
    "/order",
    response_model=OrderCheckoutResponse
)
def checkout_order(
    request:OrderCheckoutRequest,
    db:Session= Depends(get_db)
):
    products = search_products(
        db,
        request.product_name
    )

    if not products:
        raise HTTPException(
            status_code = 404,
            detail="Product not found"
        )
    
    product = products[0]

    policy = get_policy(db)
    return create_checkout_order(
        db=db,
        customer_id=request.customer_id,
        product=product,
        policy=policy,
        discount_percent= request.discount_percent
    )