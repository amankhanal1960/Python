from datetime import datetime, timezone
from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String, Numeric, Date

from app.database import Base
from app.domain.order_state_machine import (
    OrderStatus,
    validate_and_get_next_status,
)

def utcnow():
    return datetime.now(timezone.utc)

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), index=True, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(30), nullable=False, default=OrderStatus.PENDING_PAYMENT.value, index=True)
    idempotency_key = Column(String(255), nullable=False, unique=True)
    created_at = Column(Date(timezone=True), nullable=False, default=utcnow)
    updated_at = Column(Date(timezone=True), nullable=True, onupdate=utcnow)
    
    __table_args__ = (
        CheckConstraint("total_amount >= 0", name="ck_order_total_non_negative"),
        CheckConstraint(
            "status IN ('PENDING_PAYMENT', 'PAID', 'EXPIRED', 'CANCELLED', 'COMPLETED', 'REFUNDED')",
            name="ck_order_valid_status",
        ),
    )
    def change_status(self, new_status: OrderStatus) -> None:
        self.status = validate_and_get_next_status(self.status, new_status)
    
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