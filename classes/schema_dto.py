from pydantic import BaseModel
from typing import List

class Task(BaseModel):
    name: str
    priority: str

class ToDoList(BaseModel):
    category: str
    tasks: List[Task] = []

class User(BaseModel):
    email: str
    password: str