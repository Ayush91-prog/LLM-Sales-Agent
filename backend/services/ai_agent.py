import os
from strands import Agent
from strands.models.gemini import GeminiModel
from database.session import SessionLocal
from models.business import Business
from models.product import Product
from models.policy import Policy
from models.customer import Customer
from services.product_service import search_products, get_all_products
from services.customer_service import find_customer_in_message
from services.order_service import get_customer_orders
from services.ai_tools import (
    quote_tool,
    discount_tool,
    checkout_tool,
    order_tracking_tool,
    customer_history_tool,
    policy_check_tool,
    product_search_tool,
    )
from services.recommendation_service import recommend_products

if not os.getenv("GOOGLE_API_KEY"):
    raise RuntimeError(
        "GOOGLE_API_KEY environment variable is not configured."
    )

model = GeminiModel(
    model_id="gemini-2.5-flash"
)

agent = Agent(
    model=model,
    tools=[
        quote_tool,
        discount_tool,
        checkout_tool,
        order_tracking_tool,
        customer_history_tool,
        policy_check_tool,
        product_search_tool,
    ]
)

def chat(message:str, business_id: int | None=None, customer_id:int | None=None, history: list | None = None):
    db = SessionLocal()

    try:
        businesses = db.query(Business).all()
        business_map = {b.id: b for b in businesses}

        policies = db.query(Policy).all()
        policy_map = {p.business_id: p for p in policies}

        matched_products = search_products(
            db,
            message,
            business_id=business_id
        )

        if matched_products:
            context = matched_products

            recommendations = recommend_products(
                db,
                matched_products[0]
            )
            active_business_ids = {p.business_id for p in matched_products}
        else:
            context = get_all_products(db,business_id=business_id)
            recommendations = []
            active_business_ids = {p.business_id for p in context}


        product_lines = []
        for p in context:
            seller = business_map.get(p.business_id)
            seller_name = seller.name if seller else "Unknown Seller"
            product_lines.append(
                f"-Product: {p.name} | Price ₹{p.price:,.2f} | Stock: {p.stock} | Seller: {seller_name} (Seller ID:{p.business_id})"
            )
        product_text = "\n".join(product_lines) if product_lines else "No products found in the catalog."

        rec_lines = []
        for p in recommendations:
            seller = business_map.get(p.business_id)
            seller_name = seller.name if seller else "Same Seller"
            rec_lines.append(
                 f"- {p.name} | Price: ₹{p.price:,.2f} | Stock: {p.stock} (Seller: {seller_name})"
            )

        recommendation_text = "\n".join(rec_lines) if rec_lines else "None"

        policy_lines = []
        for b_id in active_business_ids:
            seller = business_map.get(b_id)
            b_name = seller.name if seller else f"Seller #{b_id}"
            pol = policy_map.get(b_id)
            if pol:
                max_disc = f"{pol.max_discount_percent}%" if pol.max_discount_percent is not None else "0%"
                min_val = f"₹{pol.min_order_value_for_discount:,.2f}" if pol.min_order_value_for_discount else "None"
                free_ship = f"₹{pol.free_shipping_over:,.2f}" if pol.free_shipping_over else "None"
                flat_ship = f"₹{pol.flat_shipping_fee:,.2f}" if pol.flat_shipping_fee else "₹0.00"
                ret_days = f"{pol.return_window_days} days" if pol.return_window_days else "No returns"
                policy_lines.append(
                    f"Seller '{b_name}' (ID: {b_id}):\n"
                    f"  - Max Discount Allowed: {max_disc}\n"
                    f"  - Min Order Value for Discount: {min_val}\n"
                    f"  - Free Shipping Over: {free_ship} (Standard Flat Fee: {flat_ship})\n"
                    f"  - Return Window: {ret_days}\n"
                    f"  - First Time Buyer Discount: {'Yes' if pol.allow_first_time_customer else 'No'}\n"
                    f"  - Bulk Purchase Allowed: {'Yes' if pol.allow_bulk_purchase else 'No'}"
                )
            else:
                policy_lines.append(f"Seller '{b_name}' (ID: {b_id}): Standard retail terms (0% discount cap, standard shipping).")
        policy_text = "\n\n".join(policy_lines) if policy_lines else "Standard marketplace policies apply."

        customer = None
        if customer_id is not None:
            customer = db.query(Customer).filter(Customer.id==customer_id).first()

        if not customer:
              matched_customers = find_customer_in_message(db,message)
              if matched_customers:
                  customer = matched_customers[0]

        if customer:
              orders = get_customer_orders(db, customer.id)
              orders_lines = [
                f"Order #{order.id} - ₹{order.total_amount:,.2f} - Status: {order.status} (Ship To: {order.shipping_address or customer.address or 'Address on file'})"
                for order in orders
               ]
              orders_text = "\n".join(orders_lines) if orders_lines else "No previous orders on record."
              total_spend = sum(order.total_amount for order in orders)
              customer_text = (
                  f"Customer ID: {customer.id}\n"
                  f"Customer Name: {customer.name}\n"
                  f"Email: {customer.email}\n"
                  f"Phone: {customer.phone}\n"
                  f"Saved Delivery Address: {customer.address or 'Registered address on file'}\n"        
                  f"Total Past Orders: {len(orders)}\n"
                  f"Total Lifetime Spend: ₹{total_spend:,.2f}"
                ) 
        else:
            customer_text = "Guest customer (Not logged in / Session expired)"
            orders_text = "No purchase history available"

        if business_id and business_id in business_map:
            single_b = business_map[business_id]
            store_identity = f"AI Sales Representative for {single_b.name}"
            brand_tone = single_b.brand_voice or "Helpful, polite, and professional"
        else:
            store_identity = "AI Marketplace Concierge (Universal Multi-Store Assistant)"
            brand_tone = "Professional, welcoming, advisory, and transparent"

        prompt = f"""
                     You are the {store_identity}.
                     Brand Tone: {brand_tone}
                     Currency: INR (₹)

                    MARKETPLACE CATALOG:
                    {product_text}

                    RECOMMENDED COMPLEMENTARY PRODUCTS (From Same Seller):
                    {recommendation_text}

                    SELLER POLICIES & NEGOTIATION RULES:
                    {policy_text}


                    Customer Profile:
                    {customer_text}

                    CUSTOMER ORDER HISTORY:
                    {orders_text}

                    Customer Message:
                    {message}

                    Operational Responsibilities:
                    1. AUTOMATIC SELLER SELECTION:
                    - When the customer asks for a product, find which seller offers it in the catalog.
                    - Mention the product and clearly state the seller's name (e.g. "We have the Samsung Galaxy S23 available from our verified seller Khalsa Enterprises for ₹45,000").
                    - You do NOT require the customer to manually select a seller. You route it automatically.
                    2. POLICY-BOUND NEGOTIATION & PRICING:
                    - Always adhere strictly to that specific seller's policy.
                    - If the customer asks for a discount, check that seller's Max Discount and Min Order Value.
                    - NEVER offer or agree to a discount higher than the seller's Max Discount.
                    - Use `discount_tool` to compute and confirm the discounted price.
                    - Use `quote_tool` when explaining the breakdown of product price, shipping fee, and potential discount.
                    3. CROSS-SELLER ISOLATION IN RECOMMENDATIONS:
                    - When suggesting 1 complementary product, only recommend products sold by the SAME seller as the primary product.
                    4. TOOL USAGE RULES:
                    - For a price breakdown or quote: Call `quote_tool(product_name=...)`.
                    - For negotiating/applying discounts: Call `discount_tool(product_name=..., discount_percent=...)`.
                    - To checkout/place an order: Call `checkout_tool(customer_name=..., product_name=..., discount_percent=...)`.
                    * CRITICAL: If a Customer Profile is present above (customer is logged in), use that customer's name directly. NEVER ask them to provide their name!
                    - To check existing order status: Call `order_tracking_tool(order_id=...)`.
                    - To inspect a customer's past orders: Call `customer_history_tool(customer_name=...)`.
                    - To search the catalog dynamically: Call `product_search_tool(query=...)`.
                    - To verify policy rules: Call `policy_check_tool(business_id=...)`.
                    - GUEST RESTRICTION: If the customer profile is "Guest customer" (not logged in), DO NOT allow checkout! Politely inform them: "To place an order, you must first log in to your registered customer account."
                    - AUTOMATIC ADDRESS BINDING: For logged-in customers, call checkout_tool(customer_name=..., product_name=..., discount_percent=...).
                    - In the checkout confirmation, state that the order will be shipped to their Saved Delivery Address.
                    - The customer NEVER has to type their address again.
                    5. CLOSING & CLARITY:
                    - Be concise, direct, and guide the customer toward completing the purchase.
                    - When an order is placed, summarize the Order ID, final price, and status clearly.
                """
        response= agent(prompt)
        return str(response)
    finally:
        db.close()