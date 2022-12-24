# fastapi相关导入
from fastapi import APIRouter, Form
# sql相关导入
from sqlalchemy import select
from database import session
from database import engine
from database import User
# 杂项导入
from email_validator import validate_email, EmailNotValidError
from passlib.context import CryptContext

router = APIRouter()
session = session()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 处理提交的新用户注册表单
@router.put("/sign/")
def sign_up(email: str = Form(), password: str = Form(), nick_name: str = Form()):
    # 校验email地址是否合法并将其标准化
    try:
        email = validate_email(email, check_deliverability=True).email
    except EmailNotValidError:
        return {'status code': 'wrong email'}
    # 检查用户是否已经注册
    stmt = select(User).where(User.email == email)
    result = session.execute(stmt)
    result = result.scalar()
    if result is not None:
        return {'status code': 'exited email'}
    else:
        # 将新用户的数据写入数据库，注意密码是经过hash的
        new_user = User(email=email, password=pwd_context.hash(password), nick_name=nick_name)
        session.add(new_user)
        session.commit()
        return {'status code': 'sign up OK'}
