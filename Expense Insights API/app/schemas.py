from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field
from app.models import TransactionType

class TransactionBase(BaseModel):
    #... means the field is strictly required, gt=0 means greater than 0
    amount: Decimal = Field(..., gt=0, description="Amount must be greater than zero")
    # min_length=0 means it prevents the user from sending empty string (like "")
    category: str = Field(..., min_length=1, description="Category cannot be empty")
    type: TransactionType
    date: date
    note: Optional[str] = Field(None, max_length=255)
    
# pass means these class inherit everything from TransactionBase
class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    created_at: datetime

class Config:
    from_attributes = True
    
class CategorySpend(BaseModel):
    category: str
    total_spent: Decimal

class MonthlyAnalyticsResponse(BaseModel):
    total_income: Decimal
    total_expenses: Decimal
    balance: Decimal
    spending_by_category: List[CategorySpend]
    transaction_count: int