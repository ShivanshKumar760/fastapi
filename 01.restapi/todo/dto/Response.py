from pydantic import BaseModel



# Response DTO
class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool