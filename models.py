from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, UniqueConstraint
from sqlmodel import Field, SQLModel


class ToDo(
    SQLModel,
    table=True,
    __table_args__=(UniqueConstraint("name")),
):
    id: Optional[int] = Field(primary_key=True, default=None, index=True)
    name: str = Field(sa_column=Column("name", String, unique=True))
    description: str
    added_on: Optional[datetime] = Field(default_factory=datetime.now)
    is_active: Optional[bool] = True
