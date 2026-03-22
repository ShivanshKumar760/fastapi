from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str

class ProjectCreate(BaseModel):
    project_name: str

class ProjectResponse(BaseModel):
    project: str
    url: str