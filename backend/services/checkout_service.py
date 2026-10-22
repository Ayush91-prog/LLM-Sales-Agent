from models.order import Order
from models.customer import Customer
from services.discount_service import apply_discount

def create_checkout_order(
        db,
        customer_id,
        product,
        policy,
        discount_percent
):
    if product.stock <= 0:
        raise ValueError("Product is out of stock")

    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    shipping_addr = customer.address if (customer and customer.address) else "Registered Address"

    pricing = apply_discount(
        product,
        policy,
        discount_percent
    )
    order = Order(
        business_id = product.business_id,
        customer_id = customer_id,
        product_id = product.id,
        total_amount=pricing["final_price"],
        status = "pending",
        shipping_address=shipping_addr
    )
    product.stock -= 1

    db.add(order)
    db.commit()
    db.refresh(order)
    db.refresh(product)

    return {
        "order_id": order.id,
        "customer_id":customer_id,
        "customer_name":customer.name if customer else "Customer",
        "shipping_address":shipping_addr,
        "product_name":product.name,
        "original_price":pricing["original_price"],
        "discount_percent":pricing["discount_percent"],
        "final_price":pricing["final_price"],
        "status":order.status
    }

