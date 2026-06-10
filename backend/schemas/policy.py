from pydantic import BaseModel

class PolicyCreate(BaseModel):
    business_id:int

    max_discount_percent: float | None=None
    min_order_value_for_discount:float | None=None

    allow_bulk_purchase: bool = False
    allow_first_time_customer: bool = False
    allow_seasonal_sale:bool = False
    allow_loyalty_reward: bool = False
    allow_price_match: bool = False
    allow_custom_reason:bool=False

    free_shipping_over:float | None=None
    flat_shipping_fee:float | None=None

    return_window_days: int | None=None
    non_refundable_categories: str| None=None

class PolicyResponse(PolicyCreate):
    id:int

    class Config:
        from_attributes = True