from typing import List
from urllib import response
from fastapi import FastAPI, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import engine, get_db

# this line automatically creates the SQLite database file and tables if they do not exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Insights API")

# get request used to monitor the applications status   
@app.get("/health", tags=["System"])
def health_check():
    return {"status": "healthy", "message": "API is running"}

# this is post request used to receive incomming user data, validate it and write a new record into a relational database
@app.post("/transactions", response_model=schemas.TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = models.Transaction(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.get("/transactions", response_model=List[schemas.TransactionResponse])
def list_transactions(db: Session = Depends(get_db)):
    return db.query(models.Transaction).all()

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