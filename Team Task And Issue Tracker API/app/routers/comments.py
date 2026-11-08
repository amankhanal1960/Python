from sqlite3 import IntegrityError

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.security import get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["Comment"]
)

# Creating a comment
@router.post("/{task_id}/comments/", status_code=status.HTTP_201_CREATED, response_model=schemas.CommentResponse)
def create_comment(
    task_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    comment_db = models.Comment(
        content = comment.content,
        task_id = task_id,
        author_id = current_user.id
    )
    db.add(comment_db)
    db.commit()
    db.refresh(comment_db)
    return comment_db

@router.get("/{task_id}/comments/", status_code=status.HTTP_200_OK, response_model=list[schemas.CommentResponse])
def get_comments(
    task_id: int, 
    db: Session = Depends(get_db),
):
    
    tasks = db.query(models.Task).filter(models.Task.id == task_id)
    if not tasks:
        raise HTTPException(status_code=404, detail="Task doesn't exists")
    
    comment_query = db.query(models.Comment).filter(models.Comment.task_id == task_id)
    comments = comment_query.all()
    
    return comments