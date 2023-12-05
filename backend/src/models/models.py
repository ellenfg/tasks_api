from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date
from ..database import Base
import datetime

class Task(Base):
    __tablename__ = "Tasks"

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    description = Column(String(255))
    due_date = Column(Date, nullable=False, default=datetime.date.today)

# Task:
# task_id (unique identifier)
# title (task title)
# description (task description)
# due_date (due date of the task)