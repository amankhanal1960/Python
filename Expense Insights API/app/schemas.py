from datetime import date, datetime
from decimal import Decimal
from typing import Optional
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
    
class BudgetBase(BaseModel):
    model_config= {"from_attributes": True}
    category: str = Field(..., min_length=1, description="Category cannot be empty")
    month: int = Field(..., ge=1, le=12, description="Month must be between 1 and 12")
    year: int = Field(..., ge=2000, description="Year must be a valid four digit integer")
    budget_amount: Decimal = Field(..., gt=0, description="Budget amount must be greater than zero")

class BudgetCreate(BudgetBase):
    pass

class BudgetUpdate(BudgetBase):
    budget_amount : Decimal = Field(..., gt=0, description="Budget amount must be greater than zero")

class BudgetResponse(BudgetBase):
    id: int
    
class Config:
    from_attributes = True
    
class CategorySpend(BaseModel):
    category: str
    total_spent: Decimal

class MonthlyAnalyticsResponse(BaseModel):
    total_income: Decimal
    total_expenses: Decimal
    balance: Decimal
    spending_by_category: list[CategorySpend]
    transaction_count: int
    
class BudgetReportItem(BaseModel):
    category: str
    budget_amount: Decimal
    amount_spent: Decimal
    Amount_remaining: Decimal
    status: str # within the budget or over budget
    
class MonthlyBudgetReportResponse(BaseModel):
    month: int
    year: int
    report: list[BudgetReportItem]