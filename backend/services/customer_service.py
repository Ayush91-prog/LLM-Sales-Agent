from sqlalchemy.orm import Session
from models.customer import Customer

def search_customer(db:Session, query:str):
    customers = db.query(Customer).all()

    query_lower = query.lower()

    for customer in customers:
        if customer.name.lower() in query_lower:
            return customer
        
    return None