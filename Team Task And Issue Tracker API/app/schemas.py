from datetime import datetime
from pydantic import BaseModel, EmailStr

# USER SPACE
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    
    model_config = {"from_attributes": True}
    
# PROJECT SPACE
class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    
class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    owner_id: int
    created_at: datetime
    
    model_config = {"from_attributes": True}
    
class ProjectUpdate(BaseModel):
    name: str
    description: str | None = None
    
# TASK SPACE
class TaskCreate(BaseModel):
    title: str
    description: str | None
    priority: str | None
    due_date: datetime | None
    asignee_id: int

class TaskResponse(BaseModel):
    id: int
    title: str
    status: str 
    priority: str
    due_date: datetime
    project_id: int
    creator_id: int | None
    asignee_id: int | None
    created_at: datetime
    
class TaskUpdate(BaseModel):
    title: str
    status: str
    priority: str