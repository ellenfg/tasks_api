from datetime import date
from pydantic import BaseModel


class Task(BaseModel):
    task_id: int = None
    title: str
    description: str
    due_date: date

class CreateTask(BaseModel):
    title: str
    description: str
    due_date: date

    class Config:
        from_attributes = True

