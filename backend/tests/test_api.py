import pytest

def test_admin_register_and_login(client):
    """
    Test full admin onboarding and JWT authentication flow.
    """
    # Register admin
    reg_payload = {
        "name":"Aryan Gupta",
        "email":"aryan23@gmail.com",
        "password":"aryan23",
        "business_name":"Aryan Tech"
    }

    reg_res = client.post("/auth/admin/register", json=reg_payload)
    assert reg_res.status_code == 200
    reg_data = reg_res.json()
    assert "access_token" in reg_data
    assert "admin_code" in reg_data

    # login admin using email
    login_payload = {
        "identifier":"aryan23@gmail.com",
        "password":"aryan23"
    }
    login_res = client.post("/auth/admin/login",json=login_payload)
    assert login_res.status_code == 200
    login_data = login_res.json()
    assert "access_token" in login_data
    assert login_data["user_type"] == "admin"

def test_admin_create_and_fetch_products(client):
    """
    Test that an authenticated admin can add a product and fetch their store catalog
    """

    # Register admin to get token
    reg_res = client.post("/auth/admin/register", json={
        "name":"Bob Admin",
        "email":"bob@gmail.com",
        "password":"password123",
        "business_name":"Bob Books"
    })

    token = reg_res.json()["access_token"]
    headers = {"Authorization":f"Bearer {token}"}

    # add product to the catalog 
    prod_payload = {
        "business_id":1,
        "name":"Python Programming Guide",
        "price":599.0,
        "stock":15
    }
    create_res = client.post("/products/", json=prod_payload, headers=headers)
    assert create_res.status_code == 200
    created_prod = create_res.json()
    assert created_prod["name"] == "Python Programming Guide"

def test_api_checkout_returns_400_when_out_of_stock(client, db_session):
    """
    Test the POST /checkout/order gracefully returns 400 when an item is out of stock"""
    from models.business import Business
    from models.customer import Customer
    from models.product import Product

    # Set Business , customer , and out of stock product
    b = Business(name="Toy Store")
    db_session.add(b)
    db_session.commit()

    cust = Customer(name="Sameer", email="sameer2@gmail.com")
    prod = Product(business_id=b.id,name="Sold out Lego", price=1200.0,stock=0)
    db_session.add_all([cust,prod])
    db_session.commit()

    checkout_payload = {
        "customer_id":cust.id,
        "product_name":"Sold Out Lego",
        "discount_percent":0.0
    }
    res = client.post("/checkout/order", json=checkout_payload)

    assert res.status_code == 400
    assert "out of stock" in res.json()["detail"].lower()

def test_admin_bulk_upload_products(client):
    """Test that an authenticated admin can bulk upload multiple catalog items."""

    reg_res = client.post("/auth/admin/register",json={
        "name":"Aneesh Kumar",
        "email":"aneesh2@gmail.com",
        "password":"aneesh123",
        "business_name":"Aneesh Superstore"
    })

    token = reg_res.json()["access_token"]
    headers = {"Authorization":f"Bearer {token}"}

    bulk_payload = [
        {"name":"Wireless Mouse", "price":499.0, "stock":20,"business_id":1},
        {"name": "Mechanical Keyboard", "price": 2499.0, "stock": 10, "business_id": 1},
        {"name": "Gaming Headset", "price": 1899.0, "stock": 5, "business_id": 1}
    ]

    res = client.post("/products/bulk", json=bulk_payload, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 3
    assert data[0]["name"] == "Wireless Mouse"
    assert data[1]["name"] == "Mechanical Keyboard"
    assert data[2]["name"] == "Gaming Headset"

def test_get_products_filtered_by_business(client, db_session):
    """Test that public GET/products?business_id=x only returns products for that business."""
    from models.business import Business
    from models.product import Product

    b1 = Business(name="Store Alpha")
    b2 = Business(name="Store Beta")
    db_session.add_all([b1,b2])
    db_session.commit()

    p1 = Product(business_id=b1.id,name="Alpha Shoes", price=100.0,stock=5)
    p2 = Product(business_id=b2.id,name="Beta headphones", price=200.0,stock=3)
    db_session.add_all([p1,p2])
    db_session.commit()

    res = client.get(f"/products/?business_id={b1.id}")
    assert res.status_code == 200
    items = res.json()
    assert len(items) == 1
    assert items[0]["name"] == "Alpha Shoes"
