from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from fastapi.middleware.cors import CORSMiddleware
from database.database import engine
from database.base import Base
from api import ai

import models

from api.products import router as products_router
from api.business import router as business_router
from api.policy import router as policies_router
from api.customers import router as customers_router
from api.orders import router as orders_router
from api.quotes import router as quote_router
from api.discounts import router as discount_router
from api.checkout import router as checkout_router
from api.analytics import router as analytics_router


#Create tables
Base.metadata.create_all(bind=engine)



app = FastAPI(
    title="AI Sales Agent API",
    description="Backend API for AI Sales Agent",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://sweet-bombolone-71c76f.netlify.app",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai.router)
app.include_router(products_router)
app.include_router(business_router)
app.include_router(policies_router)
app.include_router(customers_router)
app.include_router(orders_router)
app.include_router(quote_router)
app.include_router(discount_router)
app.include_router(checkout_router)
app.include_router(analytics_router)

@app.get("/")
def home():
    return {
        "message":"AI Sales Agent Backend Running"
    }
