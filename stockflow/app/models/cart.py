from datetime import datetime, timezone
from tkinter import CASCADE

from sqlalchemy import CheckConstraint, UniqueConstraint, Column, ForeignKey, Integer, DateTime
from app.database import Base

def utcnow():
    return datetime.now(timezone.utc)

class Cart(Base):
    __tablename__ = "carts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)

class CartItem(Base):
    __tablename__ = "cart_items"
    
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete=CASCADE), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    
    __tablea_args__ = (
        UniqueConstraint("cart_id", "product_id", name="uq_cart_product"),
        CheckConstraint("quantity > 0", name="ck_cart_item_quantity_positive"),
    )