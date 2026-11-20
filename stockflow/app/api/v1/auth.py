from sqlalchemy.exc import IntegrityError

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas, models
from app.services.auth_services import (
    create_access_token,
    get_password_hash,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=schemas.user.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(user: schemas.user.UserCreate, db: Session = Depends(get_db)):
    try:
        hashed_pwd = get_password_hash(user.password)
        db_user = models.User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_pwd,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        db.rollback()
        existing_user = (
            db.query(models.User)
            .filter(
                (models.User.email == user.email)
                | (models.User.username == user.username)
            )
            .first()
        )
        if existing_user:
            raise HTTPException(
                status_code=400, detail="User with this email already exists"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database integrity error: {str(e.orig)}",
        )


@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    db_user = (
        db.query(models.User).filter(models.User.username == form_data.username).first()
    )

    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_payload = {"sub": db_user.username}
    access_token = create_access_token(data=token_payload)

    return {"access_token": access_token, "token_type": "bearer"}
