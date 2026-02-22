from fastapi import FastAPI, HTTPException, Depends, Request, responses
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import User, URL
from schemas import UserRegister, UserLogin, URLCreate, URLOut
from auth import hash_password, verify_password, create_access_token, verify_token
from utils import generate_short_code


app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(request: Request, db: Session = Depends(get_db)):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    try:
        scheme, token = auth_header.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid header format")
    
    email = verify_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


# User Registration
@app.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed = hash_password(user.password)
    db_user = User(name=user.username, email=user.email, password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User registered successfully"}

# User Login
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}


@app.post("/urls", response_model=URLOut)
def create_url(url: URLCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    code = generate_short_code()
    # Ensure uniqueness
    while db.query(URL).filter(URL.short_code == code).first():
        code = generate_short_code()
    
    db_url = URL(original_url=url.original_url, short_code=code, user_id=current_user.id)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

# Get all URLs of current user
@app.get("/urls", response_model=list[URLOut])
def get_urls(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    urls = db.query(URL).filter(URL.user_id == current_user.id).all()
    return urls

# Redirect short URL
@app.get("/{code}")
def redirect_url(code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_code == code).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return responses.RedirectResponse(url=url.original_url)