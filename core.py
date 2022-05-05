from typing import List

import sqlalchemy
from sqlmodel import select

from database import get_session
from models import ToDo
from task_repository import TaskRepository


def add_task_to_database(name: str, description: str) -> bool:
    """Add a task to database"""
    todo = ToDo(name=name, description=description)
    try:
        task_repository.add(todo)
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
    return [task_repository.get_by_id(task_id)]


def update_task_name_from_database(
    task_id: int, new_task_name: str
) -> List[ToDo]:
    """Update task name from database using id"""
    return [task_repository.update_name(task_id, new_task_name)]


def update_task_description_from_database(
    task_id: int, new_task_description: str
) -> List[ToDo]:
    """Update task description from database using id"""
    return [task_repository.update_description(task_id, new_task_description)]


def delete_task_from_database(task_id: int) -> bool:
    """Delete a task from database by id"""
    return task_repository.delete(task_id)


task_repository = TaskRepository(get_session())
