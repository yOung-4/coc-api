from passlib.context import CryptContext
from dependencies.plugins.get_env import get_env
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = get_env().secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = get_env().access_token_expire_minutes
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", )


def get_hashed_password(password: str, ) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str, ) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
