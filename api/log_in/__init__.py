from fastapi import APIRouter, Depends
from database import session
from database import User
from sqlalchemy import select
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from typing import Union


router = APIRouter()
session = session()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "d63edd05abbb5bfcdf4a34c320685142fc479a2f78b3c88e3619c5c4bd31bfb6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post('/auth/log-in')
def log_in(data: OAuth2PasswordRequestForm = Depends()):
    result = session.execute(
        select(User).where(User.email == data.username)
    )
    result = result.scalar()
    if not pwd_context.verify(data.password, result.password):
        return {'status code': 'wrong password'}
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": data.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
