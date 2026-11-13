from fastapi import FastAPI
from sqlalchemy import engine
from app import models
from app.database import engine
from app.routers import auth, comments, dashboard, projects, tasks


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Team Task and Issue Tracker API")
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(comments.router)
app.include_router(dashboard.router)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "Healthy", "message": "The API is running"}