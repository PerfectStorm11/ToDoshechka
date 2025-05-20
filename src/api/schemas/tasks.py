import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Task(BaseModel):
    pass

class TaskSchema(BaseModel):
    title: str
    description: Optional[str]
    start_date: datetime.datetime
    end_date: Optional[datetime.datetime] = Field(default=None, nullable=True)
    reward_points: Optional[int] = Field(default=0, nullable=True)
    is_done: Optional[bool]

class TaskGetSchema(TaskSchema):
    id: int

class TaskUpdateSchema(TaskSchema):
    id: int
    title: Optional[str]
    start_date: Optional[datetime.datetime]


