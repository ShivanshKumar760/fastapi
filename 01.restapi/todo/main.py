from fastapi import FastAPI
from dto.CreateRequest import TodoCreateRequest as CreateRequest
from dto.UpdateRequest import TodoUpdateRequest as UpdateRequest
from service.TodoService import * 

app = FastAPI()

@app.get("/todos")
def read_todos():
    return get_all()

@app.get("/todos/{todo_id}")
def read_todo(todo_id: int):
    todo = get_by_id(todo_id)
    if todo:
        return todo
    return {"error": "Todo not found"}

# how to get url query parameters in fastapi
@app.get("/search")
def search_todos(q: str = ""):
    # results = [todo for todo in get_all() if q.lower() in todo.title.lower()]
    # i dont want one line lambda functions
    results = []
    for todo in get_all():
        if q.lower() in todo.title.lower():
            results.append(todo)
    return results

@app.post("/todos")
def create_todo(todo_data: CreateRequest):
    return create(todo_data)

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo_data: UpdateRequest):
    updated_todo = update(todo_id, todo_data)
    if updated_todo:
        return updated_todo
    return {"error": "Todo not found"}

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    delete(todo_id)
    return {"message": "Todo deleted"}

