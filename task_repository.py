from sqlmodel import select

from models import ToDo
from serializers import ToDoIn


class TaskRepository:
    def __init__(self, session):
        self.session = session

    def add(self, task: ToDo):
        with self.session as session:
            session.add(task)
            session.commit()
            session.refresh(task)
        return task

    def get_by_id(self, task_id: int):
        with self.session as session:
            result = session.exec(
                statement=select(ToDo).where(ToDo.id == task_id)
            )
            task: ToDo = result.one()
        return task

    def update(self, task_id: int, todo_in: ToDoIn):
        with self.session as session:
            result = session.exec(
                statement=select(ToDo).where(ToDo.id == task_id)
            )
            task: ToDo = result.one()
            task.name = todo_in.name
            task.description = todo_in.description
            session.commit()
            session.refresh(task)
            return task

    def delete(self, task_id: int):
        with self.session as session:
            result = session.exec(
                statement=select(ToDo).where(ToDo.id == task_id)
            )
            task = result.one()
            session.delete(task)
            session.commit()
        return True

    def update_name(self, task_id: int, new_name):
        with self.session as session:
            result = session.exec(
                statement=select(ToDo).where(ToDo.id == task_id)
            )
            task: ToDo = result.one()
            task.name = new_name
            session.commit()
            session.refresh(task)
            return task

    def update_description(self, task_id: int, new_description):
        with self.session as session:
            result = session.exec(
                statement=select(ToDo).where(ToDo.id == task_id)
            )
            task: ToDo = result.one()
            task.description = new_description
            session.commit()
            session.refresh(task)
            return task
