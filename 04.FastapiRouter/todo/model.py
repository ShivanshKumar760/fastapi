from pydantic import BaseModel

#Request DTO 
class TodoCreateRequest(BaseModel):
    title: str

#Response DTO
class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool

#Update Request DTO
class TodoUpdateRequest(BaseModel):
    title: str
    completed: bool