from models.product import Product

def recommend_products(
        db,
        current_product
):
    return (
        db.query(Product)
        .filter(
            Product.id != current_product.id
        )
        .limit(3)
        .all()
    )