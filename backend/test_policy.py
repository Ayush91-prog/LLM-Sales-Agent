from database.session import SessionLocal
from services.customer_service import search_customer
from services.order_service import get_customer_orders

db = SessionLocal()

customer = search_customer(db,"Rahul Sharma")
orders = get_customer_orders(db, customer.id)

print(customer.name)
for order in orders:
    print(order.total_amount)