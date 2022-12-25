from fastapi import APIRouter, Depends

from database import session
from database import User
from sqlalchemy import select

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import timedelta

from depends.token_log_in import ACCESS_TOKEN_EXPIRE_MINUTES
from depends.create_access_token import create_access_token

router = APIRouter()
session = session()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post('/token')
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
