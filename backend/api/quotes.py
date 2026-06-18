from fastapi import (APIRouter,Depends,HTTPException)
from sqlalchemy.orm import Session
from database.dependencies import get_db
from schemas.quote import (QuoteRequest,QuoteResponse)
from services.product_service import (search_products)
from services.policy_service import(get_policy)
from services.quote_service import generate_quote

router =APIRouter(
    prefix="/quotes",
    tags=["Quotes"]
)

@router.post(
    "/generate",
    response_model=QuoteResponse
)
def create_quote(
    request: QuoteRequest,
    db: Session = Depends(get_db)
):
    products = search_products(
        db,
        request.product_name
    )
    if not products:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    product = products[0]
    policy = get_policy(db)
    quote = generate_quote(
        product,
        policy
    )
    return quote