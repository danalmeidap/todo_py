from typing import List

from fastapi import FastAPI, Response, status

from core import get_task_by_id_from_database, get_tasks_from_database
from database import get_session
from models import ToDo
from serializers import ToDoIn, ToDoOut
from task_repository import TaskRepository

api = FastAPI(title="ToDo")


@api.get("/tasks", response_model=List[ToDoOut])
def list_tasks():
    """list tasks from database"""
    return get_tasks_from_database()


@api.get("/tasks/{task_id}", response_model=ToDoOut)
async def get_product_by_id(task_id: int, response: Response):
    task = get_task_by_id_from_database(task_id)
    if len(task) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        task = task_repository.get_by_id(task_id)
        return task


@api.post("/tasks", response_model=ToDoOut)
async def add_task(todo_in: ToDoIn, response: Response):
    task = ToDo(**todo_in.dict())
    task_repository.add(task)
    response.status_code = status.HTTP_201_CREATED
    return task


@api.put(
    "/tasks/{task_id}/",
    response_model=ToDoOut,
)
async def update_task(
    task_id: int,
    todo_in: ToDoIn,
    response: Response,
):
    task = get_task_by_id_from_database(task_id)
    if len(task) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        task = task_repository.update(task_id, todo_in)
        response.status_code = status.HTTP_200_OK
    return task if task else response


@api.delete("/tasks/{task_id}")
async def delete_task(task_id: int, response: Response):
    task = get_task_by_id_from_database(task_id)
    if len(task) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        if task_repository.delete(task_id):
            response.status_code = status.HTTP_204_NO_CONTENT
        return (
            f"Task id {task_id} deleted"
            if response.status_code == status.HTTP_204_NO_CONTENT
            else response
        )


task_repository = TaskRepository(get_session())
