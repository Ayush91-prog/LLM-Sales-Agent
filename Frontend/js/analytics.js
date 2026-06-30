console.log("Analytics Page Loaded");
const loadBtn = document.querySelector("#loadAnalyticsBtn");

if(loadBtn){
    loadBtn.addEventListener(
        "click",
        loadAnalytics
    );
}

async function loadAnalytics(){
    const businessId = document.querySelector("#businessId").value;

    if(!businessId){
        alert("Enter Business ID");
        return;
    }
    try{
        const response = await fetch(
            `${API_BASE_URL}/analytics/business/${businessId}`
        );
        if(!response.ok){
            throw new Error("Failed to load Analytics")
        }
        const analytics = await response.json();
        renderAnalytics(analytics);
    }
    catch(error){
        console.error(error);
        alert("Error loading analytics");
    }
}

function renderAnalytics(data){
    document.querySelector("#totalRevenue").textContent = `₹${data.total_revenue}`;
    document.querySelector("#totalOrders").textContent = `${data.total_orders}`;
    document.querySelector("#averageOrderValue").textContent = `₹${data.average_order_value}`;
    const table = document.querySelector("#topProductsTable");
    table.innerHTML="";
    if(!data.top_selling_products || data.top_selling_products.length===0){
        table.innerHTML=`
        <tr>
            <td colspan="2">
               NO sales Data available
            </td>
        </tr>
        `;
        return;
    }
    data.top_selling_products.forEach(product=> {
        table.innerHTML +=`
             <tr>
                <td>${product.product_name}</td>
                <td>${product.sales_count}</td>
            </tr>
        `;
    });
}