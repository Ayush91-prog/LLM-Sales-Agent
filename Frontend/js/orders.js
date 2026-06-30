console.log("Orders Page Loaded");
const orderTableBody = document.querySelector('#ordersTableBody');
const statValues = document.querySelectorAll(".stat-value");

async function loadOrders() {
    try {
        const response = await fetch(
            `${API_BASE_URL}/orders/`
        );
        const orders = await response.json();
        renderOrders(orders);
    } catch (error) {
        console.error(error);
    }
}
function renderOrders(orders) {

    const totalOrders = orders.length;

    const totalRevenue = orders.reduce(
        (sum, order) =>
            sum + Number(order.total_amount),
        0
    );

    const averageOrderValue =
        totalOrders > 0
            ? (totalRevenue / totalOrders).toFixed(2)
            : 0;

    statValues[0].textContent =
        totalOrders;

    statValues[1].textContent =
        `₹${totalRevenue}`;

    statValues[2].textContent =
        `₹${averageOrderValue}`;

    orderTableBody.innerHTML = "";

    if (orders.length === 0) {

        orderTableBody.innerHTML = `
            <tr>
                <td colspan="6">
                    No Orders Found
                </td>
            </tr>
        `;
        return;
    }
    orders.forEach((order) => {
        orderTableBody.innerHTML += `
            <tr>
                <td>${order.id}</td>
                <td>${order.customer_id}</td>
                <td>${order.customer_name}</td>
                <td>₹${order.total_amount}</td>
                <td>${order.status}</td>
                <td>${new Date(order.created_at)
                .toLocaleDateString()}</td>
            </tr>
        `;
    });
}

loadOrders();