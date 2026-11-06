from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status, Response
from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy.exc import IntegrityError
from app.security import get_current_user
from app import schemas, models

router = APIRouter(
    prefix="/task",
    tags=["task"]
)

@router.post("/{project_id}", status_code=status.HTTP_201_CREATED, response_model=schemas.TaskResponse)
def create_task(
    task: schemas.TaskCreate,
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    try:
        db_task = models.Task(
            title=task.title,
            description=task.description,
            creator_id= current_user.id,
            project_id= project_id
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Task with this name already exists"
        )


@router.get("/project/{project_id}", response_model=list[schemas.TaskResponse], status_code=status.HTTP_200_OK)
def get_tasks(
    project_id: int,
    #  Query(......) cleaner url ?status=completed
    task_status: Literal["todo", "in-progress", "completed"] | None = Query(default=None, alias="status"),
    sort_by: Literal["due_date", "priority", "created_at"] = Query(default ="created_at"),
    
    sort_order: Literal["asc", "desc"] = "asc",
    
    limit: int = Query(default=10, ge=1, le=100),
    skip: int = Query(default=0, ge=0),
    
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    sort_columns = {
    "due_date": models.Task.due_date,
    "priority": models.Task.priority,
    "created_at": models.Task.created_at
    }

    task_query = db.query(models.Task).filter(
        models.Task.project_id == project_id,
        models.Project.owner_id == current_user.id
    )
    if task_status:
        task_query = task_query.filter(
            models.Task.status == task_status
        )
        
    selected_column = sort_columns.get(sort_by, models.Task.created_at)
    
    if sort_order == "asc":
        task_query = task_query.order_by(selected_column.asc())
    else:
        task_query = task_query.order_by(selected_column.desc())
    tasks = task_query.limit(limit).offset(skip).all()
    
    return tasks

@router.put("/{task_id}", response_model=schemas.TaskResponse, status_code=status.HTTP_200_OK)
def update_task(
    task_id: int,
    updated_task: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    task_query = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.creator_id == current_user.id 
    )
    task = task_query.first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.title = updated_task.title
    task.status = updated_task.status
    task.priority = updated_task.priority
    db.commit()
    db.refresh(task)
    return task

# @router.patch("/task/{task_id}/assignee")
    
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    task_query = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.creator_id == current_user.id
    )
    task = task_query.first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_query.delete(synchronize_session=False)
    db.commit()
    return Response(status.HTTP_204_NO_CONTENT)
