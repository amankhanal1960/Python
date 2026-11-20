import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, computed_field


class Productreate(BaseModel):
    name: str
    description: str
    price: Decimal = Field(..., ge=0)
    category_id: int | None = None
    initial_stock: int = Field(default=0, ge=0)


class InventoryResponse(BaseModel):
    stock_quantity: int
    reserved_quantity: int
    available_stock: int
    version: int

    @computed_field
    @property
    def available_stock(self) -> int:
        return self.stock_quantity - self.reserved_quantity

    model_config = ConfigDict(from_attributes=True)


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: Decimal
    category_id: int | None
    created_at: datetime
    inventory: InventoryResponse | None = None

    model_config = ConfigDict(from_attributes=True)


class CategoryCreate(BaseModel):
    name: str
    slug: str
    parent_id: int | None = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    parent_id: int | None

    model_congif = ConfigDict(from_attributes=True)


class ProductWithInventoryResponse(BaseModel):
    product: ProductResponse
    inventory: InventoryResponse | None = None
