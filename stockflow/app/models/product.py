from datetime import datetime, timezone
from sqlalchemy import (
    CheckConstraint,
    Text,
    Column,
    ForeignKey,
    Integer,
    String,
    Numeric,
    DateTime,
)

from app.database import Base


def utcnow():
    return datetime.now(timezone.utc)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    slug = Column(String(120), unique=True, index=True, nullable=False)
    parent_id = Column(
        Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    category_id = Column(
        Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)

    __table_args__ = (
        CheckConstraint("price >= 0", name="ck_product_price_non_negetive"),
    )


class Inventory(Base):
    __tablename__ = "inventories"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(
        Integer,
        ForeignKey("products.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    stock_quantity = Column(Integer, nullable=False, default=0)
    reserved_quantity = Column(Integer, nullable=False, default=0)
    version = Column(Integer, nullable=False, default=1)

    __table_args__ = (
        CheckConstraint("stock_quantity >= 0", name="ck_inventory_stock_non_negative"),
        CheckConstraint(
            "reserved_quantity >= 0", name="ck_inventory_reserved_non_negative"
        ),
        CheckConstraint(
            "stock_quantity >= reserved_quantity", name="ck_inventory_available_stock"
        ),
    )
