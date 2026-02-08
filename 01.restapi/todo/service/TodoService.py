from dto.CreateRequest import TodoCreateRequest as CreateRequest
from dto.Response import TodoResponse
from dto.UpdateRequest import TodoUpdateRequest as UpdateRequest
from typing import List
from models.Todo import todos, current_id

def get_all():
    return todos

def get_by_id(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    return None

def create(todo_data: CreateRequest):
    global current_id
    new_todo = TodoResponse(id=current_id, title=todo_data.title, completed=False)
    todos.append(new_todo)
    current_id += 1
    return new_todo

def update(todo_id: int, todo_data: UpdateRequest):
    for todo in todos:
        if todo.id == todo_id:
            todo.title = todo_data.title
            todo.completed = todo_data.completed
            return todo
    return None

def delete(todo_id: int):
    global todos
    todos = [todo for todo in todos if todo.id != todo_id]

