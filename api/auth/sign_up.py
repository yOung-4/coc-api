from fastapi import APIRouter, HTTPException
from configs.database.user_list import user_list_class
from configs.database.connection import SessionLocal
from passlib.context import CryptContext
import uuid
import re


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post('/sign-up', tags=['auth'])
def sign_up(input_user_basic_info:  user_list_class, db_session: SessionLocal):
    #check the email
    if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", input_user_basic_info.email):
        db_session.select()
