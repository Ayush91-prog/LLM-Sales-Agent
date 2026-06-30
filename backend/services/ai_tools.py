from strands import tool
from database.session import SessionLocal

from services.product_service import search_products
from services.policy_service import get_policy
from services.customer_service import find_customer_in_message

from services.quote_service import generate_quote
from services.discount_service import apply_discount
from services.checkout_service import create_checkout_order



@tool
def quote_tool(product_name:str):
    """
Generate a sales quote for a product.
Args:
    product_name: Name of the product.
"""
    db = SessionLocal()

    try:
        products = search_products(
            db, product_name
        )
        if not products:
            return{
                "error":"Product not found"
            }
        product = products[0]
        policy = get_policy(db,product.business_id)
        return generate_quote(
            product,
            policy
        )
    finally:
        db.close()

@tool
def discount_tool(
        product_name:str,
        discount_percent:float
):
    
    """
    Apply a discount to a product.

    Args:
         product_name: Name of the product.
         discount_percent: Discount percentage.
    """
    db = SessionLocal()

    try:
        products = search_products(
            db,
            product_name
        )
        if not products:
            return{
                "error":"Product not found"
            }
        product = products[0]
        policy = get_policy(db,product.business_id)
        return apply_discount(
            product,
            policy,
            discount_percent
        )
    finally:
        db.close()

@tool
def checkout_tool(
        customer_name:str,
        product_name:str,
        discount_percent:float = 0
):
    """
    Create an order.
    
    Args:
        customer_name: Customer name.
        product_name: Product name.
        discount_percent: Discount percentage.
    """
    
    db = SessionLocal()
    try:
        products=search_products(
            db, product_name
        )
        if not products:
            return{
                "error":"Product not found"
            }
        customers = find_customer_in_message(
            db, 
            customer_name
        )
        if not customers:
            return {
                "error":"Customer not found"
            }
        
        product = products[0]
        customer = customers[0]
        policy = get_policy(db,product.business_id)

        return create_checkout_order(
            db=db,
            customer_id=customer.id,
            product=product,
            policy=policy,
            discount_percent=discount_percent
        )
    finally:
        db.close()