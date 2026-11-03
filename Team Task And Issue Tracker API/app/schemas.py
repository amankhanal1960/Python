from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    model_config = {"from_attributes": True}

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime