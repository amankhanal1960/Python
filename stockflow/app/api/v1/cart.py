from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.services.auth_services import get_current_user

router = APIRouter(prefix="/cart", tags=["Shopping Cart"])

def get_or_create_cart(user_id: int, db: Session) -> models.Cart:
    