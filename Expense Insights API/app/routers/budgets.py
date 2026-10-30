from sqlite3 import IntegrityError

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import List

from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/budget",
    tags=["Budget"]
)

# 1. CREATE A BUDGET
@router.post("", response_model=schemas.BudgetResponse, status_code=status.HTTP_201_CREATED)
def create_budget(budget: schemas.BudgetCreate, db: Session = Depends(get_db)):
    try:
        db_budget = models.Budget(**budget.model_dump())
        db.add(db_budget)
        db.commit()
        db.refresh(db_budget)
        return db_budget
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="A budget for this category in this specific month and year already exists"
        )
# 2. LIST BUDGETS (filtered by month and the date)
@router.get("", response_model=List[schemas.BudgetResponse]) 
def list_budgets(
    month: int,
    year: int,
    db: Session = Depends(get_db)
):
    return db.query(models.Budget).filter(
        models.Budget.month == month, 
        models.Budget.year == year
    ).all()
    
# 3. UPDATE a budget
@router.put("/{budget_id}", response_model=schemas.BudgetResponse)
def update_budget(
    budget_id: int,
    updated_data: schemas.BudgetUpdate,
    db: Session = Depends(get_db)
):
    budget_query = db.query(models.Budget).filter(models.Budget.id == budget_id)
    budget = budget_query.first()
    
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    budget_query.update(updated_data.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(budget)
    return budget
     
@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget(
    budget_id: int,
    db: Session = Depends(get_db)
):
    budget_query = db.query(models.Budget).filter(models.Budget.id == budget_id)
    budget = budget_query.first()
    
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    
    budget_query.delete(synchronize_session=False)
    db.commit()
    return Response(status.HTTP_204_NO_CONTENT)
