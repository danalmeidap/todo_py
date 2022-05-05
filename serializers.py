from datetime import datetime

from pydantic import BaseModel


class ToDoOut(BaseModel):
    id: int
    name: str
    description: str
    added_on: datetime


class ToDoIn(BaseModel):
    name: str
    description: str
