from fastapi import Depends

from sqlalchemy import select
from database import session
from database import User

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "d63edd05abbb5bfcdf4a34c320685142fc479a2f78b3c88e3619c5c4bd31bfb6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

session = session()


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return {'status code': 'wrong token'}
    except JWTError:
        return {'status code': 'wrong token'}
    session.execute(
        select(User).where(User.email == username)
    )
    result = session.scalar()
    if result is None:
        return {'status code': 'wrong token'}
    return username
