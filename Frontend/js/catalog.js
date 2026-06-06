console.log("Catalog Page Loaded");

const productList =
    document.querySelector("#productList");

const totalProducts =
    document.querySelector("#totalProducts");

const inventoryValueElement =
    document.querySelector("#inventoryValue");

const lowStockItemsElement =
    document.querySelector("#lowStockItems");

const products =
    JSON.parse(localStorage.getItem("products")) || [];

// Total Products
if (totalProducts) {
    totalProducts.textContent = products.length;
}

// Inventory Value
const inventoryValue = products.reduce(
    (sum, product) =>
        sum + (product.price * product.stock),
    0
);

// Low Stock Items
const lowStockItems = products.filter(
    product => product.stock < 10
).length;

// Update Stats Cards
if (inventoryValueElement) {
    inventoryValueElement.textContent =
        `₹${inventoryValue}`;
}

if (lowStockItemsElement) {
    lowStockItemsElement.textContent =
        lowStockItems;
}

// Product List
if (productList) {

    if (products.length === 0) {

        productList.innerHTML = `
            <div class="empty-state">
                <h4>No Products in Catalog</h4>
                <p>
                    Upload your catalog on the Business Setup page to start selling
                </p>
            </div>
        `;

    } else {

        productList.innerHTML = "";

        products.forEach((product) => {

            productList.innerHTML += `
                <div class="card" style="margin-top:15px;">
                    <h3>${product.name}</h3>
                    <p>Price: ₹${product.price}</p>
                    <p>Stock: ${product.stock}</p>
                </div>
            `;

        });

    }

}