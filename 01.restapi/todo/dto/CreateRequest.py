from pydantic import BaseModel


# Request DTO (like CreateTodoRequest in Spring)
class TodoCreateRequest(BaseModel):
    title: str