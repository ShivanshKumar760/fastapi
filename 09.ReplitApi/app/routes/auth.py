from fastapi import APIRouter , Depends , HTTPException
from sqlalchemy.orm import Session
from app.db.database import  SessionLocal
from app.db.models import User
from app.core.security import verify_password, hash_password, create_token, decode_token


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(username:str , password:str , db:Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")
    else:
        """
        in js :
        const newEntity = new UserEntity({
        username: req.body.username,
        password:bcrypt.hashSync(req.body.password, 10),
        });
        const savedEntity = await newEntity.save();
        """
        #so in js we have mongoose which is a odm which let us
        #create new instance of the model and then call save() to persist it in the database
        #here in python we have sqlalchemy which is an orm which let us create new instance of the model and then add it to the session and commit it to persist it in the database
        new_user = User(username=username, password=hash_password(password))
        db.add(new_user)
        db.commit()
    return {"message":"User registered successfully"}


@router.post("/login")
def login(username:str , password:str , db:Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password , user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_token({"sub": user.username})
    return {"access_token": token}
