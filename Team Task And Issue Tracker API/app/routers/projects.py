from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from sqlalchemy.exc import IntegrityError
from app.security import get_current_user
router = APIRouter(
    prefix="/project",
    tags=["Project"]
)

# create a project
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ProjectResponse)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    try:
        db_project = models.Project(
            name=project.name,
            description=project.description,
            owner_id=current_user.id
        )
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Project with this name already exists"
        )

@router.get("", response_model=list[schemas.ProjectResponse], status_code=status.HTTP_200_OK)
def get_projects(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    project_query = db.query(models.Project).filter(models.Project.owner_id == current_user.id)
    projects = project_query.all()
    
    return projects

@router.put("/{project_id}", response_model=schemas.ProjectResponse, status_code=status.HTTP_200_OK)
def update_project(
    project_id: int,
    updated_project: schemas.ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    project_query = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == current_user.id
        )
    project = project_query.first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project.name = updated_project.name
    project.description = updated_project.description
    db.commit()
    db.refresh(project)
    return project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    project_query = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == current_user.id
    )
    project = project_query.first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project_query.delete(synchronize_session=False)
    db.commit()
    return Response(status.HTTP_204_NO_CONTENT)