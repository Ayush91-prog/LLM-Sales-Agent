from strands import Agent
from strands.models.gemini import GeminiModel
from dotenv import load_dotenv
from database.session import SessionLocal
from services.product_service import (get_all_products, search_products)
from services.policy_service import get_policy
from services.customer_service import search_customer
from services.order_service import get_customer_orders
load_dotenv()

model = GeminiModel(
    model_id="gemini-2.5-flash"
)

agent = Agent(
    model=model
)

def chat(message:str):
    db = SessionLocal()

    try:
        products = search_products(
            db,
            message
        )

        if products:
            context = products
        else:
            context = get_all_products(db)


        product_text = "\n".join(
            [
                f"{p.name} - ₹{p.price} - Stock: {p.stock}"
                for p in context
            ]
        )

        policy = get_policy(db)
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
        
        customer = search_customer(db,message)
        if customer:
              orders = get_customer_orders(db,customer.id)
              customer_text = f"""
                                  Customer Name: {customer.name}
                                  Email: {customer.email}
                                  Phone: {customer.phone}
                                  Total Orders: {len(orders)}
                                  Total Spend: {sum(order.total_amount for order in orders)}
                            """
        else:
            customer_text = "No matching customer found"

        prompt = f"""
                    Available Products:

                    {product_text}

                    Business Polcies:

                    {policy_text}

                    Customer Information:

                    {customer_text}

                    Customer Question:

                    {message}

                    You are an expert AI Sales Agent

                    Your goals are:
                    1. Answer customer questions accurately.
                    2. Recommend relevant products when appropriate.
                    3. Suggest 1-2 related produts when they may benefit the customer.
                    4. Suggest a premium alternative when it provides additional value.
                    5. Mention discounts, loyalty rewards, and free shipping when applicable.
                    6. Never invent products, prices, stock levels, customers, orders, or policies.
                    7. Keep recommendations concise and helpful.
                    8. Focus on helping the customer make a purchase decision.

                    Use the provided business data to answer
                """
        response= agent(prompt)
        return str(response)
    finally:
        db.close()