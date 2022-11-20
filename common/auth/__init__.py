from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Union
from configs.database import db


class TokenData(BaseModel):
    username: Union[str, None] = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "88b8b0585635b57cb47e92f2906723380f8a86022375e4e7c1727748b486dee1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

db_conn = db()


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"}, )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    cur = db_conn.create()
    cur.execute('SELECT uuid FROM user_list WHERE email = (%s)', (token_data.username,))
    db_result = cur.fetchall()
    if db_result == []:
        cur.close
        db_conn.commit(cur)
        raise credentials_exception
    cur.close
    db_conn.commit(cur)
    return db_result[0][0]
