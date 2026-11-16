from datetime import datetime, timezone
from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String, Numeric, Date

from app.database import Base

def utcnow():
    return datetime.now(timezone.utc)

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), index=True, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(30), nullable=False, default="PENDING_PAYMENT", index=True)
    idempotency_key = Column(String(255), nullable=False, unique=True)
    created_at = Column(Date(timezone=True), nullable=False, default=utcnow)
    updated_at = Column(Date(timezone=True), nullable=True, onupdate=utcnow)
    
    __table_args__ = (
        CheckConstraint("total_amount >= 0", name="ck_order_total_non_negative"),
    )
    
class orderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("order.id", ondelete="CASCADE"), index=True, nullable=False)
    product_id = Column(Integer, ForeignKey("product.id", ondelete="RESTRICT"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    
    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_order_item_quantity_positive"),
        CheckConstraint("unit_price >= 0", name="ck_order_item_quantity_positive")
    )