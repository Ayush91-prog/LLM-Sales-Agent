def apply_discount(
        product,
        policy,
        discount_percent: float
):
    max_discount = (
        policy.max_discount_percent or 0
    )

    if discount_percent > max_discount:
        discount_percent = max_discount

    discount_amount = (
        product.price*discount_percent/100
    )

    final_price = (
        product.price - discount_amount
    )

    return {
        "product_name":product.name,
        "original_price":product.price,
        "discount_percent":discount_percent,
        "discount_amount":discount_amount,
        "final_price":final_price
    }