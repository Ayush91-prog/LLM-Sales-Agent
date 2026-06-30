console.log("Policies Page Loaded");
const saveButton =
    document.querySelector(".primary-btn");
if (saveButton) {
    saveButton.addEventListener("click", async () => {
        const policyData = {
            business_id: Number(
                document.querySelector("#businessId").value
            ),
            max_discount_percent: 
                document.querySelector("#maxDiscount").value
                ? Number(
                    document.querySelector("#maxDiscount").value
                )
            :null,
            min_order_value_for_discount:
                document.querySelector("#minOrderValue").value
                ? Number(
                    document.querySelector("#minOrderValue").value
                )
                :null,
            allow_bulk_purchase:
                document.querySelector("#allowBulkPurchase").checked,

            allow_first_time_customer:
                document.querySelector("#allowFirstTimeCustomer").checked,

            allow_seasonal_sale:
                document.querySelector(
                    "#allowSeasonalSale"
                ).checked,

            allow_loyalty_reward:
                document.querySelector(
                    "#allowLoyaltyReward"
                ).checked,

            allow_price_match:
                document.querySelector(
                    "#allowPriceMatch"
                ).checked,

            allow_custom_reason:
                document.querySelector(
                    "#allowCustomReason"
                ).checked,

            free_shipping_over: 
                document.querySelector(
                    "#freeShippingOver").value
                ? Number(
                    document.querySelector("#freeShippingOver").value
                )
                :null,

            flat_shipping_fee:
                document.querySelector("#flatShippingFee").value
                ? Number(
                    document.querySelector("#flatShippingFee").value
                )
                :null,

            return_window_days:
                document.querySelector("#returnWindowDays").value
                ? Number(
                    document.querySelector("#returnWindowDays").value
                )
                :null,

            non_refundable_categories:
                document.querySelector(
                    "#nonRefundableCategories"
                ).value
        };
        try {
            const response = await fetch(
                `${API_BASE_URL}/policies/`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type":
                            "application/json"
                    },
                    body: JSON.stringify(
                        policyData
                    )
                }
            );
            if (!response.ok) {

                const error =
                    await response.json();

                throw new Error(
                    error.detail
                );
            }
            const data =
                await response.json();

            console.log(data);

            alert(
                "Policy saved successfully"
            );
        }catch (error) {
            console.error(error);
            alert(error.message);
        }
    }
    );
}