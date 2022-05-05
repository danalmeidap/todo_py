from typing import List

from fastapi import FastAPI, Response, status
from sqlmodel import select

from core import get_task_by_id_from_database, get_tasks_from_database
from database import get_session
from models import ToDo
from serializers import ToDoIn, ToDoOut

api = FastAPI(title="ToDo")


@api.get("/tasks", response_model=List[ToDoOut])
def list_tasks():
    """list tasks from database"""
    taks = get_tasks_from_database()
    return taks


@api.get("/tasks/{task_id}", response_model=ToDoOut)
async def get_product_by_id(task_id: int, response: Response):
    task = get_task_by_id_from_database(task_id)
    if len(task) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        with get_session() as session:
            statement = select(ToDo).where(ToDo.id == task_id)
            results = session.exec(statement)
            task = results.one()
            session.refresh(task)
        response.status_code = status.HTTP_200_OK
    return task if task else response


@api.post("/tasks", response_model=ToDoOut)
async def add_task(todo_in: ToDoIn, response: Response):
    task = ToDo(**todo_in.dict())
    with get_session() as session:
        session.add(task)
        session.commit()
        session.refresh(task)
    response.status_code = status.HTTP_201_CREATED
    return task


@api.put(
    "/tasks/{task_id}/{new_task_name}/{new_task_description}",
    response_model=ToDoOut,
)
async def update_task(
    task_id: int,
    new_task_name: str,
    new_task_description: str,
    response: Response,
):
    task = get_task_by_id_from_database(task_id)
    if len(task) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        with get_session() as session:
            result = session.exec(
                statement=select(ToDo).where(ToDo.id == task_id)
            )
            task = result.one()
            task.name = new_task_name
            task.description = new_task_description
            session.commit()
            session.refresh(task)
        response.status_code = status.HTTP_200_OK
    return task if task else response


@api.delete("/tasks/{task_id}")
async def delete_task(task_id: int, response: Response):
    task = get_task_by_id_from_database(task_id)
    if len(task) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        with get_session() as session:
            result = session.exec(
                statement=select(ToDo).where(ToDo.id == task_id)
            )
            task = result.one()
            session.delete(task)
            session.commit()
            response.status_code = status.HTTP_204_NO_CONTENT
        return (
            f"Task id {task_id} deleted"
            if response.status_code == status.HTTP_204_NO_CONTENT
            else response
        )
