from pydantic import BaseModel

class UserRegistrationDTO(BaseModel):
    username: str
    email: str
    password: str

class UserLoginDTO(BaseModel):
    username: str
    password: str

class PostRequestDTO(BaseModel):
    title: str
    content: str


class PostResponseDTO(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int

    class Config:
        orm_mode = True