from sqlalchemy.orm import Session
from sqlalchemy import func

from models.order import Order
from models.product import Product

def get_total_revenue(
        db:Session,
        business_id:int
):
    revenue = (
        db.query(
            func.sum(Order.total_amount)
        )
        .filter(
            Order.business_id == business_id
        )
        .scalar()
        or 0
    )
    return revenue or 0

def get_total_orders(
        db:Session,
        business_id:int
):
    return (
        db.query(Order)
        .filter(
            Order.business_id == business_id
        )
        .count()
    )

def get_average_order_value(
        db:Session,
        business_id:int
):
    total_revenue = get_total_revenue(
        db,
        business_id
    )
    total_orders = get_total_orders(
        db,
        business_id
    )
    if total_orders == 0:
        return 0
    
    return round(
        total_revenue/total_orders,
        2
    )

def get_top_selling_products(db, business_id, limit=5):
    products = (
        db.query(Product.name, func.count(Order.id).label("sales_count"))
        .join(Order, Product.id == Order.product_id)
        .filter(Order.business_id == business_id)
        .group_by(Product.id, Product.name)
        .order_by(func.count(Order.id).desc())
        .limit(limit)
        .all()
    )
    return [{"product_name": p.name, "sales_count": p.sales_count} for p in products]

def get_sales_report(db, business_id):
    return {
        "business_id": business_id,
        "total_revenue": get_total_revenue(db, business_id),
        "total_orders": get_total_orders(db, business_id),
        "average_order_value": get_average_order_value(db, business_id),
        "top_selling_products": get_top_selling_products(db, business_id),
    }