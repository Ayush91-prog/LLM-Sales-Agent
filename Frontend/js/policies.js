console.log("Policies Page Loaded");

function getAuthHeaders() {
    const token = localStorage.getItem("admin_token");
    return {
        "Content-Type": "application/json",
        "Authorization": token ? `Bearer ${token}` : ""
    };
}

async function loadExistingPolicy() {
    try {
        const res = await fetch(`${API_BASE_URL}/policies/my`, {
            headers: getAuthHeaders()
        });
        if (!res.ok) return; 
        const policy = await res.json();
        if (document.querySelector("#maxDiscount")) document.querySelector("#maxDiscount").value = policy.max_discount_percent ?? "";
        if (document.querySelector("#minOrderValue")) document.querySelector("#minOrderValue").value = policy.min_order_value_for_discount ?? "";
        if (document.querySelector("#freeShippingOver")) document.querySelector("#freeShippingOver").value = policy.free_shipping_over ?? "";
        if (document.querySelector("#flatShippingFee")) document.querySelector("#flatShippingFee").value = policy.flat_shipping_fee ?? "";
        if (document.querySelector("#returnWindowDays")) document.querySelector("#returnWindowDays").value = policy.return_window_days ?? "";
        if (document.querySelector("#nonRefundableCategories")) document.querySelector("#nonRefundableCategories").value = policy.non_refundable_categories ?? "";

        if (document.querySelector("#allowBulkPurchase")) document.querySelector("#allowBulkPurchase").checked = !!policy.allow_bulk_purchase;
        if (document.querySelector("#allowFirstTimeCustomer")) document.querySelector("#allowFirstTimeCustomer").checked = !!policy.allow_first_time_customer;
        if (document.querySelector("#allowSeasonalSale")) document.querySelector("#allowSeasonalSale").checked = !!policy.allow_seasonal_sale;
        if (document.querySelector("#allowLoyaltyReward")) document.querySelector("#allowLoyaltyReward").checked = !!policy.allow_loyalty_reward;
        if (document.querySelector("#allowPriceMatch")) document.querySelector("#allowPriceMatch").checked = !!policy.allow_price_match;
        if (document.querySelector("#allowCustomReason")) document.querySelector("#allowCustomReason").checked = !!policy.allow_custom_reason;
    } catch (err) {
        console.error("Could not fetch existing policy:", err);
    }
}

const saveButton = document.querySelector(".primary-btn") || document.querySelector("#savePolicyBtn");
if (saveButton) {
    saveButton.addEventListener("click", async () => {
        const maxDisc = document.querySelector("#maxDiscount")?.value;
        const minOrder = document.querySelector("#minOrderValue")?.value;
        const freeShip = document.querySelector("#freeShippingOver")?.value;
        const flatShip = document.querySelector("#flatShippingFee")?.value;
        const retDays = document.querySelector("#returnWindowDays")?.value;

        const policyData = {
            max_discount_percent: maxDisc ? Number(maxDisc) : null,
            min_order_value_for_discount: minOrder ? Number(minOrder) : null,
            free_shipping_over: freeShip ? Number(freeShip) : null,
            flat_shipping_fee: flatShip ? Number(flatShip) : null,
            return_window_days: retDays ? Number(retDays) : null,
            non_refundable_categories: document.querySelector("#nonRefundableCategories")?.value || null,

            allow_bulk_purchase: document.querySelector("#allowBulkPurchase")?.checked || false,
            allow_first_time_customer: document.querySelector("#allowFirstTimeCustomer")?.checked || false,
            allow_seasonal_sale: document.querySelector("#allowSeasonalSale")?.checked || false,
            allow_loyalty_reward: document.querySelector("#allowLoyaltyReward")?.checked || false,
            allow_price_match: document.querySelector("#allowPriceMatch")?.checked || false,
            allow_custom_reason: document.querySelector("#allowCustomReason")?.checked || false
        };

        try {
            const response = await fetch(`${API_BASE_URL}/policies/`, {
                method: "POST",
                headers: getAuthHeaders(),
                body: JSON.stringify(policyData)
            });

            if (!response.ok) {
                const error = await response.json().catch(() => ({}));
                throw new Error(error.detail || "Failed to save policy");
            }

            alert("Policy saved successfully!");
        } catch (error) {
            console.error(error);
            alert(`Error saving policy: ${error.message}`);
        }
    });
}

document.addEventListener("DOMContentLoaded", loadExistingPolicy);
