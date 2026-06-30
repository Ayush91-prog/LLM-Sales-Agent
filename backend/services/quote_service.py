def generate_quote(
        product,
        policy
):
    shipping_fee = 0
    discount_available = False
    estimated_total= product.price

    if(
        policy.free_shipping_over is not None
        and product.price < policy.free_shipping_over
    ):
        shipping_fee = (
            policy.flat_shipping_fee or 0
        )
    if policy.max_discount_percent is not None:
        discount_available = True


    estimated_total = product.price+shipping_fee
    

    return {
        "product_name": product.name,
        "price": product.price,
        "shipping_fee": shipping_fee,
        "discount_available": discount_available,
        "max_discount_percent": (
            policy.max_discount_percent
            if discount_available
            else None
        ),
        "estimated_total": estimated_total
    }