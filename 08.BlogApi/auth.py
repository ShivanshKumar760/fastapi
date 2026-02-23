from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError , jwt 

SECRET_KEY= "sgjbsbfewbfbewvsfsbsbgjbgisb"
ALGORITHM = "HS256"
ACCESS_TOEKN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOEKN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")#to get the user id from the token
    except JWTError:
        return None
    