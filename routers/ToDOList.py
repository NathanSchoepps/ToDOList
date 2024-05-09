from fastapi import APIRouter, Depends, HTTPException
from typing import List
import uuid
from classes.schema_dto import Task, ToDoList
from database.firebase import db
from routers.Auth import get_current_user

router = APIRouter(tags=["ToDoLists"])

# Exemples de listes de tâches
todo_lists = [
    ToDoList(category="Personnel", tasks=[Task(name="Lire un livre", priority="High")]),
    ToDoList(category="Travail", tasks=[Task(name="Envoyer rapport", priority="Medium")]),
]

@router.get("/todolists/", response_model=List[ToDoList])
async def get_all_todo_lists(userData: int = Depends(get_current_user)):
    firebase_object = db.child("users").child(userData["uid"]).child("ToDo").get().val()
    todo_lists = [value for value in firebase_object.values()]
    return todo_lists

@router.get("/todolists/{category}", response_model=List[ToDoList])
async def get_todo_lists_by_category(category: str, userData: int = Depends(get_current_user)):
    firebase_object = db.child("users").child(userData["uid"]).child("ToDo").get().val()
    todo_lists = [value for value in firebase_object.values()]
    lists = [t for t in todo_lists if t["category"] == category]
    return lists

@router.post("/todolists/", response_model=ToDoList)
async def create_todo_list(todo_list: ToDoList, userData: int = Depends(get_current_user)):
    firebase_object = db.child("users").child(userData["uid"]).child("ToDo").get().val()
    if firebase_object is None:
        firebase_object = {}
    todo_list_id = str(uuid.uuid4())
    firebase_object[todo_list_id] = todo_list.dict()
    db.child("users").child(userData["uid"]).child("ToDo").set(firebase_object)
    return todo_list

@router.post("/todolists/{category}", response_model=ToDoList)
async def add_task_to_todo_list(category: str, task: Task, userData: int = Depends(get_current_user)):
    firebase_object = db.child("users").child(userData["uid"]).child("ToDo").get().val()
    todo_lists = [value for value in firebase_object.values()]
    for todo_list in todo_lists:
        if todo_list["category"] == category:
            todo_list["tasks"].append(task.dict())
            db.child("users").child(userData["uid"]).child("ToDo").set(firebase_object)
            return todo_list
    raise HTTPException(status_code=404, detail="ToDo list not found")

@router.patch("/todolists/{category}", response_model=ToDoList)
async def patch_todo_list(category: str, updated_category: str, userData: int = Depends(get_current_user)):
    firebase_object = db.child("users").child(userData["uid"]).child("ToDo").get().val()
    todo_lists = [value for value in firebase_object.values()]
    for todo_list in todo_lists:
        if todo_list["category"] == category:
            todo_list["category"] = updated_category
            db.child("users").child(userData["uid"]).child("ToDo").set(firebase_object)
            return todo_list
    raise HTTPException(status_code=404, detail="ToDo list not found")

@router.delete("/todolists/{category}", response_model=ToDoList)
async def delete_todo_list_by_category(category: str, userData: int = Depends(get_current_user)):
    firebase_object = db.child("users").child(userData["uid"]).child("ToDo").get().val()
    if firebase_object:
        for key, todo_list in firebase_object.items():
            if todo_list.get("category") == category:
                db.child("users").child(userData["uid"]).child("ToDo").child(key).remove()
                return todo_list
    raise HTTPException(status_code=404, detail="ToDo list not found")

@router.patch("/todolists/{category}/tasks/{task_name}", response_model=ToDoList)
async def patch_task_from_todo_list(category: str, task_name: str, updated_name: str, userData: int = Depends(get_current_user)):
    firebase_object = db.child("users").child(userData["uid"]).child("ToDo").get().val()
    todo_lists = [value for value in firebase_object.values()]
    for todo_list in todo_lists:
        if todo_list["category"] == category:
            for task in todo_list["tasks"]:
                if task["name"] == task_name:
                    task["name"] = updated_name
                    db.child("users").child(userData["uid"]).child("ToDo").set(firebase_object)
                    return todo_list
    raise HTTPException(status_code=404, detail="Task not found in the ToDo list")

@router.delete("/todolists/{category}/tasks/{task_name}", response_model=ToDoList)
async def delete_task_from_todo_list(category: str, task_name: str, userData: int = Depends(get_current_user)):
    firebase_object = db.child("users").child(userData["uid"]).child("ToDo").get().val()
    todo_lists = [value for value in firebase_object.values()]
    for todo_list in todo_lists:
        if todo_list["category"] == category:
            for task in todo_list["tasks"]:
                if task["name"] == task_name:
                    todo_list["tasks"].remove(task)
                    db.child("users").child(userData["uid"]).child("ToDo").set(firebase_object)
                    return todo_list
    raise HTTPException(status_code=404, detail="Task not found in the ToDo list")
