import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, Enum, UniqueConstraint
from app.database import Base

class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    category = Column(String, index=True, nullable=False) # nullable means the database will reject the entry if this is missing
    note = Column(String, nullable=True)
    date = Column(Date, nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
class Budget(Base):
    __tablename__ = "budgets"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True, nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    budget_amount = Column(Numeric(10, 2), nullable=False)
    
    __table_args__ = (
        UniqueConstraint('category', 'month', 'year', name='_category_month_year_uc'),
    )
    
        