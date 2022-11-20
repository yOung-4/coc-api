from datetime import datetime, timedelta
from typing import Union
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from configs.database import db

SECRET_KEY = ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

db_conn = db()

class TokenData(BaseModel):
    username: Union[str, None] = None
class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"},)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    cur = db_conn.create()
    cur.execute('SELECT FROM user_list WHERE email = (%s)', (token_data.username,))
    list = cur.fetchall()
    if list == []:
        raise credentials_exception
    return list[0]

@router.post("/login/", tags=['auth'])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    cur = db_conn.create()
    cur.execute\
        ('SELECT password FROM user_list WHERE email = (%s)', (form_data.username,))
    passwd = cur.fetchall()
    if passwd != [] and pwd_context.verify(form_data.password, passwd[0][0]) is True:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"},)

@router.post("/login-token", tags=['auth'])
def login_with_token(current_user = Depends(get_current_user)):
   return current_user