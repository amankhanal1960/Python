from app.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Date


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(Date, nullable=False)

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(Date, nullable=False)
    
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, nullable=False, primary_key=True, index=True)
    description = Column(String, nullable=True)
    title = Column(String, index=True)
    status = Column(String, default="todo")
    priority = Column(String, default="medium")
    due_date = Column(Date, nullable=True)
    created_at = Column(Date, nullable=False)
    
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    asignee_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    body = Column(String, nullable=False)
    created_at = Column(Date, nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    