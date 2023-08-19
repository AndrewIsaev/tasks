from datetime import datetime

from pydantic import BaseModel

from src.tasks.models import StatusEnum


class TaskSchema(BaseModel):
    id: int
    name: str
    description: str
    status: StatusEnum
    employee_id: int
    parent_id: int | None
    deadline: datetime


class TaskCreateSchema(BaseModel):
    name: str
    description: str
    status: StatusEnum
    employee_id: int
    parent_id: int | None
    deadline: datetime
