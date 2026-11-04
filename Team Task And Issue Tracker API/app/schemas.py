from datetime import datetime
from pydantic import BaseModel, EmailStr

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