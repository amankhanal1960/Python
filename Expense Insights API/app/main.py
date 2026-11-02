from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from datetime import date
from app import models, schemas
from app.database import engine, get_db
from app.routers import analytics, budgets
import io
import csv
from fastapi.responses import StreamingResponse

# this line automatically creates the SQLite database file and tables if they do not exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Insights API")

app.include_router(analytics.router)

app.include_router(budgets.router)

# get request used to monitor the applications status   
@app.get("/health", tags=["System"])
def health_check():
    return {"status": "Healthy", "message": "API is running!"}

# this is post request used to receive incomming user data, validate it and write a new record into a relational database
@app.post("/transactions", response_model=schemas.TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = models.Transaction(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.get("/transactions", response_model=List[schemas.TransactionResponse], tags=["Transactions"])
def list_transactions(
    category: Optional[str] = None,
    type: Optional[models.TransactionType] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code = 400,
            detail="Start date cannot be greater than end date"
        )
    # Starting with a foundational query (not executing it yet)
    query = db.query(models.Transaction)    
    # layer on filters only if the user actually passed them
    if category:
        #.ilike() makes the search case-insensitive
        query = query.filter(models.Transaction.category.ilike(category))
    if type:
        query = query.filter(models.Transaction.type == type)
    if start_date:
        query = query.filter(models.Transaction.date >= start_date)
    if end_date:
        query = query.filter(models.Transaction.date <= end_date)
        
    transaction = query.all()
    
    return transaction

@app.get("/transactions/{transaction_id}", response_model=schemas.TransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@app.put("/transactions/{transaction_id}", response_model=schemas.TransactionResponse)
def update_transaction(transaction_id: int, updated_data: schemas.TransactionUpdate, db: Session = Depends(get_db)):
    transaction_query = db.query(models.Transaction).filter(models.Transaction.id == transaction_id)
    transaction = transaction_query.first()
    
    if not transaction: 
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    transaction_query.update(updated_data.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(transaction)
    return transaction

@app.delete("/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction_query = db.query(models.Transaction).filter(models.Transaction.id == transaction_id)
    transaction = transaction_query.first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    transaction_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/transactions/export/csv", tags=["Transaction"])
def export_transactions_to_csv(
    category: Optional[str] = None,
    type: Optional[models.TransactionType] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    if start_date and end_date and start_date > end_date:
        raise HTTPException(status_code=400, detail="Start date cannot be after end date")
    
    query = db.query(models.Transaction)
    
    if category:
        query = query.filter(models.Transaction.category.ilike(category))
    if type:
        query = query.filter(models.Transaction.type == type)
    if start_date:
        query = query.filter(models.Transaction.date >= start_date)
    if end_date:
        query = query.filter(models.Transaction.date <= end_date)
        
    transactions = query.all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(["ID", "Amount", "Category", "Type", "Date", "Note", "Created At"])
    
    for t in transactions:
        writer.writerow([t.id, t.amount, t.category, t.type.value, t.date, t.note or "", t.created_at])
        
    output.seek(0)
        
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=filtered_transactions.csv"}
    )