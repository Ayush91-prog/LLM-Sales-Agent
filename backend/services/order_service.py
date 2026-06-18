from sqlalchemy.orm import Session
from models.order import Order

def get_customer_orders(db:Session, customer_id:int):
    return (
        db.query(Order)
        .filter(
            Order.customer_id == customer_id
        )
        .all()
    )