from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.dependencies import get_db

from models.order import Order
from models.business import Business
from models.customer import Customer

from schemas.order import(
    OrderCreate,
    OrderResponse
)

router=APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.post("/",response_model=OrderResponse)
def create_order(
    order:OrderCreate,
    db:Session = Depends(get_db)
):
    business = (
        db.query(Business)
        .filter(Business.id==order.business_id)
        .first()
    )
    if business is None:
        raise HTTPException(
            status_code=404,
            detail=f"Business with ID {order.business_id} not found"
        )
    
    customer = (
        db.query(Customer)
        .filter(Customer.id == order.customer_id)
        .first()
    )
    if customer is None:
        raise HTTPException(
            status_code=404,
            detail=f"Customer with ID {order.customer_id} not found"
        )
    
    new_order = Order(
        business_id = order.business_id,
        customer_id = order.customer_id,
        total_amount=order.total_amount
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

@router.get("/", response_model=list[OrderResponse])
def get_orders(
    db: Session = Depends(get_db)
):
    return db.query(Order).all()


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail=f"Order with ID {order_id} not found"
        )

    return order


@router.delete("/{order_id}")
def delete_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail=f"Order with ID {order_id} not found"
        )

    db.delete(order)
    db.commit()

    return {
        "message": "Order deleted successfully"
    }