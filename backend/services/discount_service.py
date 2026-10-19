def apply_discount(
        product,
        policy,
        discount_percent: float
):
    if discount_percent < 0:
        discount_percent = 0.0


    max_discount = policy.max_discount_percent if (policy and policy.max_discount_percent is not None) else 0
    min_order_value = policy.min_order_value_for_discount if (policy and policy.min_order_value_for_discount is not None) else 0.0

    if product.price < min_order_value:
        discount_percent = 0.0

    if discount_percent > max_discount:
        discount_percent = max_discount

    discount_amount = round(product.price*discount_percent / 100.0,2)

    final_price = product.price - discount_amount


    return {
        "product_name":product.name,
        "original_price":product.price,
        "discount_percent":discount_percent,
        "discount_amount":discount_amount,
        "final_price":final_price
    }