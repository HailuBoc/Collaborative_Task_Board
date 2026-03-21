from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    name: str


class UserResponse(BaseModel):
    id: str
    name: str


class TaskCreate(BaseModel):
    title: str
    status: str = "TODO"
    assigned_to: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    assigned_to: Optional[str] = None
    version: int


class TaskResponse(BaseModel):
    id: str
    title: str
    status: str
    assigned_to: Optional[str] = None
    updated_at: str
    version: int


class ConflictResponse(BaseModel):
    detail: str
    latest_task: TaskResponse
