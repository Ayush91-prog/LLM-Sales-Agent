from strands import tool
from database.session import SessionLocal

from models.order import Order
from services.product_service import search_products, get_all_products
from services.policy_service import get_policy
from services.customer_service import find_customer_in_message
from services.order_service import get_customer_orders

from services.quote_service import generate_quote
from services.discount_service import apply_discount
from services.checkout_service import create_checkout_order


@tool
def quote_tool(product_name: str):
    """
    Generate a sales quote for a product.
    Args:
        product_name: Name of the product.
    """
    db = SessionLocal()

    try:
        products = search_products(db, product_name)
        if not products:
            return {"error": "Product not found"}
        product = products[0]
        policy = get_policy(db, product.business_id)
        return generate_quote(product, policy)
    finally:
        db.close()


@tool
def discount_tool(product_name: str, discount_percent: float):
    """
    Apply a discount to a product based on store policy.

    Args:
        product_name: Name of the product.
        discount_percent: Requested discount percentage.
    """
    db = SessionLocal()

    try:
        products = search_products(db, product_name)
        if not products:
            return {"error": "Product not found"}
        product = products[0]
        policy = get_policy(db, product.business_id)
        return apply_discount(product, policy, discount_percent)
    finally:
        db.close()


@tool
def checkout_tool(customer_name: str, product_name: str, discount_percent: float = 0):
    """
    Create an order / checkout for a customer.

    Args:
        customer_name: Customer name.
        product_name: Product name.
        discount_percent: Discount percentage (optional).
    """

    db = SessionLocal()
    try:
        products = search_products(db, product_name)
        if not products:
            return {"error": "Product not found"}
        customers = find_customer_in_message(db, customer_name)
        if not customers:
            return {"error": "Customer not found"}

        product = products[0]
        customer = customers[0]
        policy = get_policy(db, product.business_id)

        return create_checkout_order(
            db=db,
            customer_id=customer.id,
            product=product,
            policy=policy,
            discount_percent=discount_percent,
        )
    finally:
        db.close()


@tool
def order_tracking_tool(order_id: int):
    """
    Track and view details of an existing order by Order ID.

    Args:
        order_id: Numeric ID of the order.
    """
    db = SessionLocal()
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return {"error": f"Order #{order_id} not found."}
        return {
            "order_id": order.id,
            "customer_name": order.customer.name if order.customer else "Unknown",
            "product_name": order.product.name if order.product else "Unknown",
            "total_amount": order.total_amount,
            "status": order.status,
            "created_at": order.created_at.isoformat() if order.created_at else None,
        }
    finally:
        db.close()


@tool
def customer_history_tool(customer_name: str):
    """
    Look up customer purchase history and order details by customer name.

    Args:
        customer_name: Name of the customer.
    """
    db = SessionLocal()
    try:
        customers = find_customer_in_message(db, customer_name)
        if not customers:
            return {"error": f"Customer '{customer_name}' not found."}
        customer = customers[0]
        orders = get_customer_orders(db, customer.id)

        return {
            "customer_id": customer.id,
            "name": customer.name,
            "email": customer.email,
            "total_orders": len(orders),
            "total_spend": sum(o.total_amount for o in orders),
            "orders": [
                {
                    "order_id": o.id,
                    "total_amount": o.total_amount,
                    "status": o.status,
                }
                for o in orders
            ],
        }
    finally:
        db.close()


@tool
def policy_check_tool(business_id: int = 1):
    """
    Check business policies including discount rules, free shipping thresholds, and return windows.

    Args:
        business_id: ID of the business (defaults to 1).
    """
    db = SessionLocal()
    try:
        policy = get_policy(db, business_id)
        if not policy:
            return {"message": "No active policies found for this business."}
        return {
            "max_discount_percent": policy.max_discount_percent,
            "min_order_value_for_discount": policy.min_order_value_for_discount,
            "allow_bulk_purchase": policy.allow_bulk_purchase,
            "allow_first_time_customer": policy.allow_first_time_customer,
            "allow_seasonal_sale": policy.allow_seasonal_sale,
            "allow_loyalty_reward": policy.allow_loyalty_reward,
            "allow_price_match": policy.allow_price_match,
            "free_shipping_over": policy.free_shipping_over,
            "flat_shipping_fee": policy.flat_shipping_fee,
            "return_window_days": policy.return_window_days,
            "non_refundable_categories": policy.non_refundable_categories,
        }
    finally:
        db.close()


@tool
def product_search_tool(query: str):
    """
    Search product catalog by name or keyword for real-time stock and pricing.

    Args:
        query: Product name or keyword to search for.
    """
    db = SessionLocal()
    try:
        products = search_products(db, query)
        if not products:
            products = get_all_products(db)

        return [
            {
                "product_id": p.id,
                "name": p.name,
                "price": p.price,
                "stock": p.stock,
            }
            for p in products
        ]
    finally:
        db.close()