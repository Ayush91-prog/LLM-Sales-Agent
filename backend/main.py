from fastapi import FastAPI

from database.database import engine
from database.base import Base

import models


from api.products import router as products_router
from api.business import router as business_router
from api.policy import router as policies_router
#Create tables
Base.metadata.create_all(bind=engine)



app = FastAPI(
    title="AI Sales Agent API",
    description="Backend API for AI Sales Agent",
    version="1.0.0"
)
app.include_router(products_router)
app.include_router(business_router)
app.include_router(policies_router)

@app.get("/")
def home():
    return {
        "message":"AI Sales Agent Backend Running"
    }
