from fastapi import FastAPI
app = FastAPI(
    title="AI Sales Agent API",
    description="Backend API for AI Sales Agent",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message":"AI Sales Agent Backend Running"
    }