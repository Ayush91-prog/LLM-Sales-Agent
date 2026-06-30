from sqlalchemy.orm import Session
from models.customer import Customer

def find_customer_in_message(db:Session, query:str):
    customers = db.query(Customer).all()

    query_lower = query.lower()

    matches = []
    for customer in customers:
        customer_name = customer.name.lower()
        if (
            customer_name in query_lower
            or query_lower in customer_name
        ):
            matches.append(customer)
        
    return matches