console.log("Orders Page Loaded");
const orderTableBody = document.querySelector('#ordersTableBody');
const statValues = document.querySelectorAll(".stat-value");
const orders = JSON.parse(localStorage.getItem("orders")) || [];

const totalOrders = orders.length;
const totalRevenue = orders.reduce(
    (sum,order) => sum + Number(order.total),
    0
);

const averageOrderValue = totalOrders > 0 ?(totalRevenue/totalOrders).toFixed(2):0;
// Update UI
if(statValues.length>=3){
    statValues[0].textContent=totalOrders;
    statValues[1].textContent=`₹${totalRevenue}`;
    statValues[2].textContent=`₹${averageOrderValue}`;
}
// Render Orders
if (orderTableBody) {
    if (orders.length===0) {
        orderTableBody.innerHTML = `
        <tr>
            <td colspan ="6" style="text-align:left;padding:14px 12px;">
                No Orders Found
            </td>
        </tr>
        `;
    }else{
        orders.forEach((order)=>{
            orderTableBody.innerHTML +=`
            <tr>
                <td>${order.orderId}</td>
                <td>${order.customerId}</td>
                <td>${order.customerName}</td>
                <td>₹${order.total}</td>
                <td>${order.status}</td>
                <td>${order.date}</td>
            </tr>
            `;
        });
}
}