from typing import List

import sqlalchemy
from sqlmodel import select

from database import get_session
from models import ToDo


def add_task_to_database(name: str, description: str) -> bool:
    """Add a task to database"""
    try:
        with get_session() as session:
            task = ToDo(**locals())
            session.add(task)
            session.commit()
    except sqlalchemy.exc.IntegrityError:
        return False
    return True


def get_tasks_from_database() -> List[ToDo]:
    """Get task list from database"""
    with get_session() as session:
        statement = select(ToDo)
        return list(session.exec(statement))


def get_task_by_id_from_database(task_id: int) -> List[ToDo]:
    """Get a task from database by id"""
    with get_session() as session:
        statement = select(ToDo).where(ToDo.id == task_id)
        return list(session.exec(statement))


def update_task_name_from_database(task_id: int, new_task_name: str) -> List[ToDo]:
    """Update task name from database using id"""
    with get_session() as session:
        statement = select(ToDo).where(ToDo.id == task_id)
        results = session.exec(statement)
        task = results.one()
        task.name = new_task_name
        session.commit()
        statement = select(ToDo).where(ToDo.id == task_id)
        return list(session.exec(statement))


def update_task_description_from_database(task_id: int, new_task_description: str) -> List[ToDo]:
    """Update task description from database using id"""
    with get_session() as session:
        statement = select(ToDo).where(ToDo.id == task_id)
        results = session.exec(statement)
        task = results.one()
        task.name = new_task_description
        session.commit()
        statement = select(ToDo).where(ToDo.id == task_id)
        return list(session.exec(statement))


def delete_task_from_database(task_id: int) -> bool:
    with get_session() as session:
        statement = select(ToDo).where(ToDo.id == task_id)
        result = session.exec(statement)
        task = result.one()
        if task.is_active:
            task.is_active = False
            session.commit()
            return True
        return False
