from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.dependencies import get_db

from models.order import Order
from models.business import Business
from models.customer import Customer
from models.product import Product

from schemas.order import(
    OrderCreate,
    OrderResponse,
    OrderStatusUpdate
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
    product = (
        db.query(Product)
        .filter(Product.id == order.product_id)
        .first()
    )
    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product with ID {order.product_id} not found"
        )
    
    new_order = Order(
        business_id = order.business_id,
        customer_id = order.customer_id,
        product_id = order.product_id,
        total_amount=order.total_amount
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return {
        "id":new_order.id,
        "business_id":new_order.business_id,
        "customer_id":new_order.customer_id,
        "product_id":new_order.product_id,
        "customer_name":customer.name,
        "total_amount":new_order.total_amount,
        "status": new_order.status,
        "created_at":new_order.created_at
    }

@router.get("/", response_model=list[OrderResponse])
def get_orders(
    db: Session = Depends(get_db)
):
    orders = db.query(Order).all()
    result = []

    for order in orders:
        result.append({
            "id": order.id,
            "business_id": order.business_id,
            "customer_id": order.customer_id,
            "product_id": order.product_id,
            "customer_name": order.customer.name,
            "total_amount": order.total_amount,
            "status": order.status,
            "created_at": order.created_at
        })
    return result   

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
    return {
        "id": order.id,
        "business_id": order.business_id,
        "customer_id": order.customer_id,
        "product_id": order.product_id,
        "customer_name": order.customer.name,
        "total_amount": order.total_amount,
        "status": order.status,
        "created_at": order.created_at
    }

@router.patch("/{order_id}/status",response_model= OrderResponse)
def update_order_status(
    order_id:int,
    status_data: OrderStatusUpdate,
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
    
    order.status = status_data.status
    db.commit()
    db.refresh(order)

    return{
        "id":order.id,
        "business_id":order.business_id,
        "customer_id": order.customer_id,
        "product_id": order.product_id,
        "customer_name": order.customer.name,
        "total_amount": order.total_amount,
        "status": order.status,
        "created_at": order.created_at
    }

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
