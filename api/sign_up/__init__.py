# fastapi相关导入
from fastapi import APIRouter, Form, HTTPException
# sql相关导入
from sqlalchemy import select
from database import session
from database import User
# 杂项导入
from verify_email import verify_email
from database import Base

router = APIRouter()


# 处理提交的新用户注册表单
@router.put("/sign/")
def sign_up(email: str = Form(), password: str = Form(), nick_name: str = Form()):
    if verify_email(email) is False:
        raise HTTPException(status_code=400, detail='email address is wrong')
    if not session.execute(select(User).where(User.email == email)):
        raise HTTPException(status_code=400, detail='email already exits')
    new_user = User(email = email, password = password, nick_name = nick_name)
    session.add(new_user)
    session.commit()
