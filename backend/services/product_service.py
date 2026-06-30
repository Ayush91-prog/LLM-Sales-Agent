# Get all products
# Get product by name
# Search products

from sqlalchemy.orm import Session
from models.product import Product

def get_all_products(db:Session):
    return db.query(Product).all()

def search_products(
        db:Session,
        query:str
):
    products = db.query(Product).all()
    query_lower = query.lower()
    matches = []
    for product in products:
        product_name = product.name.lower()
        if (
            product_name in query_lower
            or query_lower in product_name
        ):
            matches.append(product)
    return matches
        

def products_to_text(products):
    return "\n".join(
        [
            f"{p.name} - ₹{p.price} - Stock: {p.stock}"
            for p in products
        ]
    )