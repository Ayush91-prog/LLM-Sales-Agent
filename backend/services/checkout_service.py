from models.order import Order
from services.discount_service import apply_discount

def create_checkout_order(
        db,
        customer_id,
        product,
        policy,
        discount_percent
):
    pricing = apply_discount(
        product,
        policy,
        discount_percent
    )
    order = Order(
        business_id = product.business_id,
        customer_id = customer_id,
        total_amount=pricing["final_price"],
        status = "pending"
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    return {
        "order_id": order.id,
        "customer_id":customer_id,
        "product_name":product.name,
        "original_price":pricing["original_price"],
        "discount_percent":pricing["discount_percent"],
        "final_price":pricing["final_price"],
        "status":order.status
    }

