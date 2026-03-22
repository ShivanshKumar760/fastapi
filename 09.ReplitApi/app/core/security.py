from jose import jwt , JWTError
from datetime import datetime , timedelta
from passlib.context import CryptContext
from app.core.config import SECRET_KEY , ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(password:str , hashed:str):
    return pwd_context.verify(password , hashed)


#jwt section starts here
def create_token(data:dict):
    to_encode = data.copy()
    to_encode["exp"]=datetime.utcnow()+timedelta(hours=5)
    encoded_jwt = jwt.encode(to_encode , SECRET_KEY , algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token:str):
    try:
        return jwt.decode(token , SECRET_KEY , algorithms=[ALGORITHM])
    except JWTError:
        return None
