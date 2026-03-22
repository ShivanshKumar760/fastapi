from fastapi import Depends , HTTPException , status 
from fastapi.security import HTTPBearer , HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.core.security import decode_token
from app.db.models import User

security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(security) , 
    db: Session = Depends(get_db)

):
    token = creds.credentials
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(401, detail="Invalid token")
    user = db.query(User).filter(User.username == payload["sub"]).first()
    if not user:
        raise HTTPException(404, detail="User not found")
    return user