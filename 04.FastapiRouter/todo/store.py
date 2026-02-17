from typing import List, Optional
from .model import TodoResponse,TodoCreateRequest,TodoUpdateRequest

todos:List[TodoResponse] = []
current_id = 1


def get_all() -> List[TodoResponse]:
    return todos

def get_by_id(todo_id:int)-> Optional[TodoResponse]:
    for todo in todos:
        if todo.id == todo_id:
            return todo
    return None

def create_todo(request:TodoCreateRequest)->TodoResponse:
    global current_id
    todo = TodoResponse(id=current_id, title=request.title, completed=False)
    todos.append(todo)
    current_id += 1
    return todo

def update_todo(todo_id:int, request:TodoUpdateRequest)-> Optional[TodoResponse]:
    # for index, todo in enumerate(todos):
    #     if todo.id == todo_id:
    #         updated_todo = TodoResponse(id=todo_id, title=request.title, completed=request.completed)
    #         todos[index] = updated_todo
    #         return updated_todo
    todo=get_by_id(todo_id)
    if todo:
        todo.title=request.title
        todo.completed=request.completed
        return todo
    return None

def delete_todo(todo_id:int)-> bool:
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            del todos[index]
            return True
    return False