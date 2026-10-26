import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, Enum
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