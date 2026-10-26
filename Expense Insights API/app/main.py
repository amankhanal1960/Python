from fastapi import FastAPI

app = FastAPI(title="Expense Insights API")

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}