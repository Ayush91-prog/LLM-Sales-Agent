from models.product import Product

def recommend_products(
        db,
        current_product
):
    return (
        db.query(Product)
        .filter(
            Product.business_id == current_product.business_id,
            Product.id != current_product.id
        )
        .limit(3)
        .all()
    )