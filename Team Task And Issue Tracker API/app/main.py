from fastapi import FastAPI
from sqlalchemy import engine
from app import models
from app.database import engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Insights API")

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "Healthy", "message": "The API is running"}