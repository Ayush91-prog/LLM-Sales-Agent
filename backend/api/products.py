from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.dependencies import get_db
from models.product import Product
from models.business import Business
from schemas.product import ProductCreate , ProductResponse

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

# Creating product endpoint
@router.post("/",response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    business = (
        db.query(Business)
        .filter(Business.id == product.business_id)
        .first()
    )

    if not business:
         raise HTTPException(
            status_code=404,
            detail=f"Business with ID {product.business_id} not found"
        )


    new_product = Product(
        business_id=product.business_id,
        name=product.name,
        price=product.price,
        stock=product.stock
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

# Getting All products endpoint
@router.get("/",response_model=list[ProductResponse])
def get_products(
    db:Session = Depends(get_db)
):
    return db.query(Product).all()

#get product by id 
@router.get("/{product_id}",response_model=ProductResponse)
def get_product(
    product_id:int,
    db:Session = Depends(get_db)
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    
    return product

#Delete product
@router.delete("/{product_id}")
def delete_product(
    product_id:int,
    db:Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product with ID {product_id} not found"
        )
    
    db.delete(product)
    db.commit()
    return{
        "message":"Product deleted successfully"
    }