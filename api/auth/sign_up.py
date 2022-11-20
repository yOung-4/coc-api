from fastapi import APIRouter, HTTPException
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
    user_name: str

@router.post('/sign-up', tags=['auth'])
def sign_up(basic_info_for_new_user: basic_info_for_new_user):
    if re.match('^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$', basic_info_for_new_user.email):
        cur = db_conn.conn.cursor()
        cur.execute('SELECT email FROM user_list WHERE email = (%s);', (basic_info_for_new_user.email,))
        if cur.fetchall() != []:
            cur.close()
            raise HTTPException(status_code=400, detail='user already exists')
        else:
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            user_uuid = str(uuid.uuid4())
            cur.execute\
                ('''INSERT INTO user_list (email, uuid, password) VALUES(%s, %s, %s);''',
                [basic_info_for_new_user.email,
                user_uuid,
                pwd_context.hash(basic_info_for_new_user.password)])
            cur.execute\
                ('''INSERT INTO user_info (uuid, user_name, char_card_num, char_card_cache) 
                VALUES(%s, %s, 0, false)''', (user_uuid, basic_info_for_new_user.user_name,))
            cur.close()
            db_conn.commit(cur)
            return {'message': 'OK'}
    else:
        raise HTTPException(status_code=400, detail='wrong email?!')