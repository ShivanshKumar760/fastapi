from fastapi import FastAPI,Request, HTTPException, Depends
from UserLoginDTO import UserLogin
from UserRegisterDTO import UserRegister
from jwtUtil import create_access_token , verify_token
from bcryptUtil import hash_password , verify_password
from model import User, SessionLocal

app = FastAPI()

@app.post("/register")
def register(user: UserRegister):
    db = SessionLocal()
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        return {"error": "Email already registered"}
    
    hashed_password = hash_password(user.password)
    new_user = User(name=user.username, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully"}


@app.post("/login")
def login(user: UserLogin):
    db = SessionLocal()
    existing_user = db.query(User).filter(User.name == user.username).first()
    if not existing_user or not verify_password(user.password, existing_user.password):
        return {"error": "Invalid email or password"}
    
    token = create_access_token(data={"sub": existing_user.name})
    return {"access_token": token, "token_type": "bearer"}


#auth middleware
def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    try:
        scheme, token = auth_header.split()  # splits on whitespace
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")
    username = verify_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    return username



#protected route example
@app.get("/protected")
def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}! This is a protected route."}