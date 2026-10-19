from sqlalchemy.orm import Session
from models.product import Product

def get_all_products(db:Session,business_id:int | None=None):
    query = db.query(Product)
    if business_id is not None:
        query = query.filter(Product.business_id == business_id)
    return query.all()

def search_products(
        db:Session,
        query_str:str,
        business_id:int | None=None
):
    query = db.query(Product)
    if business_id is not None:
        query = query.filter(Product.business_id == business_id)

    products = query.all()
    query_lower = query_str.lower()
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