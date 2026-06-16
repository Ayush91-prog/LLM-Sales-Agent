console.log("Catalog Page Loaded");

const productList =
    document.querySelector("#productList");

const totalProducts =
    document.querySelector("#totalProducts");

const inventoryValueElement =
    document.querySelector("#inventoryValue");

const lowStockItemsElement =
    document.querySelector("#lowStockItems");


const saveProductBtn =
    document.querySelector("#saveProductBtn");

if (saveProductBtn) {
    saveProductBtn.addEventListener("click", async () => {
        const businessId =
            document.querySelector("#businessId").value;
        const productName =
            document.querySelector("#productName").value;
        const productPrice =
            document.querySelector("#productPrice").value;
        const productStock =
            document.querySelector("#productStock").value;
        if (
            !businessId ||
            !productName ||
            !productPrice ||
            !productStock
        ) {
            alert("Please fill all fields");
            return;
        }
        const productData = {
            business_id: Number(businessId),
            name: productName,
            price: Number(productPrice),
            stock: Number(productStock)
        };
        try {
            const response = await fetch(
                "http://127.0.0.1:8000/products/",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(productData)
                }
            );
            if (!response.ok) {
                throw new Error("Failed to create product")
            }
            const data = await response.json();
            console.log(data);
            alert("Product created Successfully")
            loadProducts();
            // clear form
            document.querySelector("#businessId").value = "";
            document.querySelector("#productName").value = "";
            document.querySelector("#productPrice").value = "";
            document.querySelector("#productStock").value = "";

        } catch (error) {
            console.error(error);
            alert("Error Creating Product");
        }
    });
}

async function loadProducts() {

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/products/"
        );
        if (!response.ok) {
            throw new Error("Failed to load products");
        }
        const products = await response.json();
        renderProducts(products);
    } catch (error) {
        console.error(error);
    }
}
function renderProducts(products) {

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

    if (inventoryValueElement) {
        inventoryValueElement.textContent =
            `₹${inventoryValue}`;
    }

    // Low Stock
    const lowStockItems = products.filter(
        product => product.stock < 10
    ).length;

    if (lowStockItemsElement) {
        lowStockItemsElement.textContent =
            lowStockItems;
    }

    // Product List
    if (!productList) return;
    if (products.length === 0) {
        productList.innerHTML = `
            <div class="empty-state">
                <h4>No Products in Catalog</h4>
                <p>No products found</p>
            </div>
        `;
        return;
    }

    productList.innerHTML = "";
    products.forEach(product => {
        productList.innerHTML += `
            <div class="card" style="margin-top:15px;">
                <h3>${product.name}</h3>
                <p>Price: ₹${product.price}</p>
                <p>Stock: ${product.stock}</p>
                <p>Business ID: ${product.business_id}</p>
                <button
                      onclick="deleteProduct(${product.id})"
                >
                    Delete
                </button>
            </div>
        `;
    });
}
async function deleteProduct(productId) {

    const confirmed = confirm(
        "Are you sure you want to delete this product?"
    );

    if (!confirmed) {
        return;
    }

    try {

        const response = await fetch(
            `http://127.0.0.1:8000/products/${productId}`,
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {
            throw new Error("Failed to delete product");
        }

        alert("Product deleted successfully");

        loadProducts();

    } catch (error) {

        console.error(error);

        alert("Error deleting product");
    }
}
document.addEventListener(
    "DOMContentLoaded",
    loadProducts
);