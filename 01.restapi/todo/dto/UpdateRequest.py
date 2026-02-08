from pydantic import BaseModel

# Request DTO for update
class TodoUpdateRequest(BaseModel):
    title: str
    completed: bool