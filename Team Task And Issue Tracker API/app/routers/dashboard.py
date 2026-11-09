from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone 
from app.database import get_db
from app.security import get_current_user
from app import schemas, models

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/", response_model=schemas.DashboardResponse, status_code=status.HTTP_200_OK)
def get_user_dashboard(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    now = datetime.now(timezone.utc)
    
    # Tasks that are assigned to me
    assigned_tasks = db.query(models.Task).filter(
        models.Task.assignee_id == current_user.id
    ).all()
    
    # Tasks in project that i own
    owned_tasks_ids = db.query(models.Project).filter(
        models.Project.owner_id == current_user.id
    ).subquery()
    
    project_tasks = db.query(models.Task).filter(
        models.Task.project_id.in_(owned_tasks_ids)
    ).all()
    
    all_relevant_tasks = list(set(assigned_tasks + project_tasks))
    
    overdue_tasks = []
    for task in all_relevant_tasks:
        if task.due_date and task.due_date < now and task.status != "completed":
            overdue_tasks.append(task)
            
    return{
        "assigned_tasks": assigned_tasks,
        "project_tasks": project_tasks,
        "overdue_tasks": overdue_tasks,
        "total_assigned": len(assigned_tasks),
        "total_overdue": len(overdue_tasks)
    }    
            
    