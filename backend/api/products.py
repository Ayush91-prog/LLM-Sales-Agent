from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from services.auth_service import get_current_admin
from models.admin import Admin
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
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_admin:Admin = Depends(get_current_admin)
):
    target_business_id = current_admin.business_id if current_admin.business_id else product_data.business_id
    business = (
        db.query(Business)
        .filter(Business.id == target_business_id)
        .first()
    )

    if not business:
         raise HTTPException(
            status_code=404,
            detail=f"Business with ID {target_business_id} not found"
        )


    new_product = Product(
        business_id=target_business_id,
        name=product_data.name,
        price=product_data.price,
        stock=product_data.stock
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

# Getting All products endpoint
@router.get("/",response_model=list[ProductResponse])
def get_all_products(
    db:Session = Depends(get_db)
):
    return db.query(Product).all()


@router.get("/my", response_model=list[ProductResponse])
def get_my_products(
    db:Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    return db.query(Product).filter(Product.business_id == current_admin.business_id).all()


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
    db:Session = Depends(get_db),
    current_admin:Admin = Depends(get_current_admin)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail=f"Product with ID {product_id} not found"
        )

    if product.business_id != current_admin.business_id:
        raise HTTPException(
            status_code = 403,
            detail="You do not have permission to delete this product"
        )
    
    db.delete(product)
    db.commit()
    return{
        "message":"Product deleted successfully"
    }