import pytest
from models.business import Business
from models.product import Product
from models.policy import Policy
from models.customer import Customer
from models.order import Order
from services.discount_service import apply_discount
from services.recommendation_service import recommend_products
from services.checkout_service import create_checkout_order

def test_apply_discount_respects_max_cap(db_session):
    """
    Test that customer discount request is capped at max_discount_percent.
    """

    product = Product(id=1, business_id=1, name="Running shoes", price=1000.0, stock=10)
    policy = Policy(business_id = 1, max_discount_percent=10.0, min_order_value_for_discount=500.0)

    # user asks for 25% discount
    result = apply_discount(product, policy, discount_percent=25.0)

    # Should be capped at 10% (100 INR off 1000 INR)
    assert result["discount_percent"] == 10.0
    assert result["discount_amount"] == 100.0
    assert result["final_price"] == 900.0


def test_apply_discount_checks_min_order_value(db_session):
    """
    Test that discount is Not applied if product price is below min_order_value_for_discount.
    """

    product = Product(id=2, business_id=1, name="Socks", price=300.0, stock=20)
    policy = Policy(business_id=1, max_discount_percent=15.0, min_order_value_for_discount=500.0)

    result = apply_discount(product,policy, discount_percent=10.0)

    assert result["discount_percent"] == 0.0
    assert result["final_price"] == 300.0

def test_recommend_products_strict_business_isolation(db_session):
    """Test that recommend_products Never recommends products form another store."""
    # Business 1(Shoe Store)
    b1 = Business(name="Sneaker Store")
    # b2 Electronics Store
    b2 = Business(name="Gadget Store")
    db_session.add_all([b1,b2])
    db_session.commit()

    p1 = Product(business_id=b1.id, name="Nike Air", price=5000.0, stock=5)
    p2 = Product(business_id=b1.id, name="Puma Runner", price=3000.0, stock=5)
    p3 = Product(business_id=b2.id, name="Iphone 18", price=80000.0, stock=2)

    db_session.add_all([p1,p2,p3])
    db_session.commit()

    recs = recommend_products(db_session,p1)
    rec_business_ids = [p.business_id for p in recs]

    assert all(b_id == b1.id for b_id in rec_business_ids), "Leaked another business's products in recommendations!"

def test_checkout_reduces_stock_on_success(db_session):
    """
    Test that a successful checkout reduces product stock by 1."""
    #  Setup test business , customer, and product with stock = 5
    b = Business(name="Shoe Store")
    db_session.add(b)
    db_session.commit()

    cust = Customer(name="John Doe", email="john@example.com")
    prod = Product(business_id=b.id ,name="Sneakers", price=2000.0, stock=5)
    db_session.add_all([cust,prod])
    db_session.commit()

    # checkout
    order_data = create_checkout_order(
        db=db_session,
        customer_id=cust.id,
        product=prod,
        policy=None,
        discount_percent=0.0
    )
    db_session.refresh(prod)

    assert order_data["status"] == "pending"
    assert prod.stock == 4

def test_checkout_falls_when_out_of_stock(db_session):
    """
    Test that checkout raises ValueError if product has 0 stock.
    """
    b = Business(name="Shoe Store")
    db_session.add(b)
    db_session.commit()

    cust = Customer(name="John Doe",email="john@example.com")
    prod = Product(business_id=b.id,name="Sold Out Shoes", price=1500.0, stock=0)
    db_session.add_all([cust,prod])
    db_session.commit()

    with pytest.raises(ValueError, match="Product is out of stock"):
        create_checkout_order(
            db=db_session,
            customer_id=cust.id,
            product=prod,
            policy=None,
            discount_percent=0.0
        )