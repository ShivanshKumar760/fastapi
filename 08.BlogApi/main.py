from fastapi import FastAPI, HTTPException, Depends, Request, responses
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import User, Post
from dtos import UserRegistrationDTO, UserLoginDTO, PostRequestDTO, PostResponseDTO
from auth import create_access_token, verify_token, hash_password, verify_password


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def current_user(request: Request, db: Session = Depends(get_db)):
    auth_header = request.headers.get("Authorization")
    if auth_header is None or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        scheme, token = auth_header.split(" ")
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Unauthorized")
    except ValueError:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user_id = verify_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user


@app.post("/register")
def register(user_dto: UserRegistrationDTO, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_dto.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user_dto.password)
    new_user = User(name=user_dto.username, email=user_dto.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}


@app.post("/login")
def login(user_dto: UserLoginDTO, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name == user_dto.username).first()
    if not user or not verify_password(user_dto.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/posts", response_model=PostResponseDTO)
def create_post(post_dto: PostRequestDTO, user: User = Depends(current_user), db: Session = Depends(get_db)):
    new_post = Post(title=post_dto.title, content=post_dto.content, owner_id=user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts", response_model=list[PostResponseDTO])
def get_posts(db: Session = Depends(get_db),user: User = Depends(current_user)):
    user=db.query(User).filter(User.id == user.id).first()
    posts = user.posts # we can do this cause base on the relationship we defined in the models.py file between user and posts
    #back populate will allow us to access the posts of a user directly from the user object without needing to query the posts table separately
    return posts