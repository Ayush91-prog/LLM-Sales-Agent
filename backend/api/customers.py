from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.dependencies import get_db

from models.customer import Customer

from schemas.customer import(
    CustomerCreate,CustomerResponse
)

router = APIRouter(
    prefix = "/customers",
    tags=["Customers"]
)

@router.post("/",response_model=CustomerResponse)
def create_customer(
    customer:CustomerCreate,
    db:Session = Depends(get_db)
):
    existing = db.query(Customer).filter(Customer.email == customer.email).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    new_customer = Customer(**customer.model_dump())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer

@router.get("/",response_model=list[CustomerResponse])
def get_customers(
    db:Session = Depends(get_db)
):
    return db.query(Customer).all()


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: int,
    db:Session  = Depends(get_db)
):
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )
    if customer is None:
        raise HTTPException(
            status_code=404,
            detail=f"Customer with ID {customer_id} not found"
        )
    return customer

@router.delete("/{customer_id}")
def delete_customer(
    customer_id: int,
    db:Session = Depends(get_db)
):
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail=f"Customer with ID {customer_id} not found"
        )
    
    db.delete(customer)
    db.commit()
    return{
        "message":"Customer deleted successfully"
    }