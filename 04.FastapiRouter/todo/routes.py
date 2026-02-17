from fastapi import APIRouter, HTTPException
from typing import List
from .model import TodoResponse, TodoCreateRequest, TodoUpdateRequest
from .store import get_all, get_by_id, create_todo, update_todo, delete_todo

router = APIRouter(prefix="/todos", tags=["Todos"])

@router.get("/", response_model=List[TodoResponse])
def read_todos():
    return get_all()

@router.get("/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id:int):
    todo=get_by_id(todo_id)
    if todo:
        return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@router.post("/", response_model=TodoResponse, status_code=201)
def create_new_todo(request:TodoCreateRequest):
    return create_todo(request)

@router.put("/{todo_id}", response_model=TodoResponse)
def update_existing_todo(todo_id:int, request:TodoUpdateRequest):
    todo=update_todo(todo_id, request)
    if todo:
        return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@router.delete("/{todo_id}", status_code=204)
def delete_existing_todo(todo_id:int):
    success=delete_todo(todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    