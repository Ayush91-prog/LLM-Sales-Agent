from strands import Agent
from strands.models.gemini import GeminiModel
from database.session import SessionLocal
from services.product_service import (get_all_products, search_products)
from services.policy_service import get_policy
from services.customer_service import find_customer_in_message
from services.order_service import get_customer_orders
from services.ai_tools import (quote_tool,discount_tool,checkout_tool)
from services.recommendation_service import recommend_products

import os
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
        checkout_tool
    ]
)

def chat(message:str):
    db = SessionLocal()

    try:
        products = search_products(
            db,
            message
        )

        recommendations = []
        business_id=None
        policy = None

        if products:
            business_id = products[0].business_id

            context = [
                p for p in products
                if p.business_id == business_id
            ]

            recommendations = recommend_products(
                db,
                products[0]
            )
        else:
            context = get_all_products(db)


        product_text = "\n".join(
            [
                f"{p.name} - ₹{p.price} - Stock: {p.stock}"
                for p in context
            ]
        )

        recommendation_text = "\n".join(
            [
                f"{p.name} - ₹{p.price}"
                for p in recommendations
            ]
        )

        if business_id is not None:
            policy = get_policy(db,business_id)
        else:
            policy = None

        if policy:
            policy_text =f"""
            Maximum Discount:{policy.max_discount_percent}%
            Minimum Order Value For Discount:{policy.min_order_value_for_discount}
            Bulk Purchase Allowed:{policy.allow_bulk_purchase}
            First Time Customer Discount:{policy.allow_first_time_customer}
            Seasonal Sale:{policy.allow_seasonal_sale}
            Loyalty Rewards:{policy.allow_loyalty_reward}
            Price Match:{policy.allow_price_match}
            Free Shipping Over:{policy.free_shipping_over}
            Flat Shipping Fee:{policy.flat_shipping_fee}
            Return Window:{policy.return_window_days} days
            Non Refundable Categories:{policy.non_refundable_categories}
            """
        else:
            policy_text = "No business policy available"

        
        customers = find_customer_in_message(db,message)
        if customers:
              customer =customers[0]
              orders = get_customer_orders(db,customer.id)

              orders_text = "\n".join(
                  [
                      f"Order #{order.id} - ₹{order.total_amount} - {order.status}"
                      for order in orders
                  ]
              )
              if not orders_text:
                  orders_text = "No previous orders"

              customer_text = f"""
                                  Customer Name: {customer.name}
                                  Email: {customer.email}
                                  Phone: {customer.phone}
                                  Total Orders: {len(orders)}
                                  Total Spend: {sum(order.total_amount for order in orders)}
                            """
        else:
            customer_text = "No matching customer found"
            orders_text = "No purchase history available"

        prompt = f"""
                    Available Products:

                    {product_text}

                    Recommended Products:

                    {recommendation_text}

                    Business Policies:

                    {policy_text}

                    Customer Information:

                    {customer_text}

                    Past Purchase History:
                    {orders_text}

                    Customer Question:

                    {message}

                    You are an expert AI Sales Agent

                    Your goals are:
                    1. Answer customer questions accurately.
                    2. Recommend relevant products when appropriate.
                    3. Suggest 1-2 related products when they may benefit the customer.
                    4. Suggest a premium alternative when it provides additional value.
                    5. Mention discounts, loyalty rewards, and free shipping when applicable.
                    6. Never invent products, prices, stock levels, customers, orders, or policies.
                    7. Keep recommendations concise and helpful.
                    8. Focus on helping the customer make a purchase decision.
                    9. Suggest a higher-priced alternative when appropriate.
                    10. Suggest complementary products when relevant.

                    If the user asks for:
                    - a quote, use the quote tool
                    - a discount calculation, use the discount tool
                    - order creation or checkout, use the checkout tool

                    Use the provided business data to answer
                """
        response= agent(prompt)
        return str(response)
    finally:
        db.close()