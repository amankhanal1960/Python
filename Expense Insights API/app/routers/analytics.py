from unicodedata import category

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal

from app import models, schemas
from app.database import get_db
router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.get("/summary", response_model=schemas.MonthlyAnalyticsResponse)
def get_monthly_summary(month: int, year: int, db: Session = Depends(get_db)):
    # fetch all the transactions for this specific month and year
    # extract(part, column) is a sql function that grabs the month or year from a full date
    transactions = db.query(models.Transaction).filter(
        func.extract('month', models.Transaction.date) == month,
        func.extract('year', models.Transaction.date) == year
    ).all()
    
    # default safe baseline
    total_income = Decimal('0.00')
    total_expenses = Decimal('0.00')
    category_map = {}
    
    for t in transactions:
        if t.type == models.TransactionType.INCOME:
            total_income += Decimal(str(t.amount))
        elif t.type == models.TransactionType.EXPENSE:
            total_expense += Decimal(str(t.amount))
            # if there is no category at all, initialize it
            if t.category not in category_map:
                category_map[t.category] = Decimal('0.00')
            category_map[t.category] += Decimal(str(t.amount))
    
    # format the raw category map in dict into our List[categorySpend] schema layout
    spending_by_category = [
        schemas.CategorySpend(category=cat, total_spent=amt) for cat, amt in category_map.items()
    ]
    
    balance = total_income - total_expense
    
    return schemas.MonthlyAnalyticsResponse(
        total_income=total_income, 
        total_expenses=total_expenses,
        balance=balance,
        spending_by_category=spending_by_category,
        transaction_count=len(transactions)
    )