from sys import exit
from typing import List

from core import get_tasks_from_database
from models import ToDo
from reader import read_input_as_integer, read_input_as_string


def validate_index(msg: str) -> int:
    tasks: List[ToDo] = get_tasks_from_database()
    while True:
        try:
            index = read_input_as_integer(msg)
            if 1 <= index <= len(tasks):
                return index
            else:
                print("Index value does not exist in database")
        except (ValueError, TypeError):
            print("The value must be an integer")
        except KeyboardInterrupt:
            print("Interrupted by user")
            exit(-1)


def validate_task_name(msg: str) -> str:
    tasks = get_tasks_from_database()
    names = [task.name for task in tasks]
    while True:
        try:
            task_name = read_input_as_string(msg)
            if task_name not in names:
                return task_name
            else:
                print("The task is already on database")
        except KeyboardInterrupt:
            print("Interrupted by user")
            exit(-1)


def validate_task_description(msg: str) -> str:
    tasks = get_tasks_from_database()
    descriptions = [task.description for task in tasks]
    while True:
        try:
            task_description = read_input_as_string(msg)
            if task_description not in descriptions:
                return task_description
            else:
                print("The task is already on database")
        except KeyboardInterrupt:
            print("Interrupted by user")
            exit(-1)
