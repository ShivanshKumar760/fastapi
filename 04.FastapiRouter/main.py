from fastapi import FastAPI
from todo.routes import router as todo_router

app = FastAPI(title="Todo API", version="1.0")
app.include_router(todo_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API!"}