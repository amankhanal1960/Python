from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlite3 import IntegrityError
from sqlalchemy.exc import Session
from app import models, schemas
from app.database import get_db
from app.security import get_password_hash, verify_password
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        hashed_pwd = get_password_hash(user.password)
        db_user = models.User(
            username = user.username,
            email = user.email,
            hashed_password = hashed_pwd
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        existing_user = db.query(models.User).filter(
            (models.User.email == user.email) | (models.User.username == user.username)).first()
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="User with this email already exists"
            )

@router.post("/login",)