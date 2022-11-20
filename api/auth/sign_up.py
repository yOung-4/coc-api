from fastapi import APIRouter
from pydantic import BaseModel
from configs.database import db
from passlib.context import CryptContext
import uuid
import re

router = APIRouter()
db_conn = db()

class basic_info_for_new_user(BaseModel):
    email: str
    password: str

@router.post('/sign-up', tags=['auth'])
def sign_up(basic_info_for_new_user: basic_info_for_new_user):
    if re.match('^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$', basic_info_for_new_user.email):
        cur = db_conn.conn.cursor()
        cur.execute\
            ('SELECT email FROM user_list WHERE email = (%s);', (basic_info_for_new_user.email,))
        if cur.fetchall() != []:
            cur.close()
            return {'messge': 'user existed'}
        else:
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            cur.execute\
                ('''INSERT INTO user_list (email, uuid, password) VALUES(%s, %s, %s);''',
                [basic_info_for_new_user.email,
                str(uuid.uuid4()),
                pwd_context.hash(basic_info_for_new_user.password)])
            cur.close()
            db_conn.commit(cur)
            return {'message': 'OK'}
    else:
        return {'message', 'email adress verity failed'}