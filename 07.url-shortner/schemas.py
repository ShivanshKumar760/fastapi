from pydantic import BaseModel

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class URLCreate(BaseModel):
    original_url: str

class URLOut(BaseModel):
    original_url: str
    short_code: str

    class Config:
        orm_mode = True