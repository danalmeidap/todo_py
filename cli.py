from time import sleep
from typing import List

from rich import print
from rich.console import Console
from rich.table import Table

from core import (
    add_task_to_database,
    delete_task_from_database,
    get_task_by_id_from_database,
    get_tasks_from_database,
    update_task_description_from_database,
    update_task_name_from_database,
)
from models import ToDo
from validations import validate_index, validate_task_description, validate_task_name


def task_register() -> None:
    """Add task to database"""
    name: str = str(input("Task name: ")).strip().upper()
    description: str = str(input("Task Description: ")).strip()
    if add_task_to_database(name, description):
        print("task was added")
    else:
        print("Cannot add task")
    sleep(2)
    menu()


def task_list():
    tasks = get_tasks_from_database()
    if len(tasks) > 0:
        table = generate_task_table(tasks)
        console.print(table)
    else:
        console.print("Tasks list is empty")
    sleep(2)
    menu()


def generate_task_table(tasks:ToDo):
    table: Table = Table(title="ToDo List")
    headers: List[str] = [
        "id",
        "name",
        "description",
        "added_on",
    ]
    print(type(tasks))
    for header in headers:
        table.add_column(header, style="magenta")
    for task in tasks:
        task.added_on = task.added_on.strftime("%Y-%m-%d")
        values: List[str] = [str(getattr(task, header)) for header in headers]
        table.add_row(*values)
    return table


def search_task_by_id():
    tasks = get_tasks_from_database()
    if len(tasks) > 0:
        index = validate_index("Index for searching: ")
        task = get_task_by_id_from_database(index)
        table = generate_task_table(task)
        console.print(table)
    else:
        console.print("Task list is empty")
    sleep(2)
    menu()


def update_task_name():
    tasks = get_tasks_from_database()
    if len(tasks) > 0:
        index = validate_index("Index for searching: ")
        new_task_name = validate_task_name("New name for task: ")
        task = update_task_name_from_database(index, new_task_name)
        table = generate_task_table(task)
        console.print(table)
    else:
        console.print("Task list is empty")
    sleep(2)
    menu()


def update_task_description():
    tasks = get_tasks_from_database()
    if len(tasks) > 0:
        index = validate_index("Index for searching: ")
        description = validate_task_description("New task description")
        task = update_task_description_from_database(index, description)
        table = generate_task_table(task)
        console.print(table)
    else:
        console.print("Task list is empty")
    sleep(2)
    menu()


def delete_task():
    tasks = get_tasks_from_database()
    if len(tasks) > 0:
        index = validate_index("Index for searching: ")
        if delete_task_from_database(index):
            console.print("The task was deleted")
        else:
            console.print("Operation not concluded")
    else:
        console.print("Task list is empty")
    sleep(2)
    menu()


def menu() -> None:
    print("Select an option below: ")
    print("1 - Task register")
    print("2 - Task's list")
    print("3 - Search task by id")
    print("4 - Update task name")
    print("5 - Update task description")
    print("6 - Delete task")
    print("7 - Exit")

    option: int = int(input())

    if option == 1:
        task_register()
    elif option == 2:
        task_list()
    elif option == 3:
        search_task_by_id()
    elif option == 4:
        update_task_name()
    elif option == 5:
        update_task_description()
    elif option == 6:
        delete_task()
    elif option == 7:
        print("Thank You!!")
        sleep(2)
        exit(0)
    else:
        print("Invalid Operationj")
        sleep(2)
        menu()


console = Console()
