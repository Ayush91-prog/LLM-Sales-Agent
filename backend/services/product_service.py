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
    return (
        db.query(Product)
        .filter(
            Product.name.ilike(f"%{query}%")
        )
        .all()
    )

def products_to_text(products):
    return "\n".join(
        [
            f"{p.name} - ₹{p.price} - Stock: {p.stock}"
            for p in products
        ]
    )