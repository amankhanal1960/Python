from decimal import Decimal
from turtle import st
from pydantic import BaseModel, ConfigDict, Field, computed_field


class CartItemAdd(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)


class CartItemUpdate(BaseModel):
    quantity: int = Field(..., ge=0)


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    unit_price: Decimal
    quantity: int

    @computed_field
    @property
    def sub_total(self) -> Decimal:
        return self.unit_price * self.quantity

    model_config = ConfigDict(from_attributes=True)


class CartResponse(BaseModel):
    id: int
    user_id: int
    items: list[CartItemResponse]

    @computed_field
    @property
    def total_amount(self) -> Decimal:
        return sum((item.subtotal for item in self.items), Decimal("0.00"))
