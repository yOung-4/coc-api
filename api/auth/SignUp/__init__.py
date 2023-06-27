from fastapi import APIRouter, Depends
from model.pydantic_model import sign_up_request, general_response_model
from model.database_model import Database_auth_user_list
from pony import orm
from passlib.context import CryptContext
from dependencies.get_plugins import dependencies_get_db, dependencies_get_hashed_password

router = APIRouter()


@router.put("/auth/sign-up/",)
async def sign_up(
        data: sign_up_request,
        db_conn: orm.Database = Depends(dependencies_get_db),
        get_hashed_password: CryptContext.hash = Depends(dependencies_get_hashed_password),
        response: general_response_model = Depends(general_response_model),
):
    with db_conn:
        # 检查邮箱是否已经被占用
        query = orm.select(
            query for query in Database_auth_user_list if query.email == data.email
        )
        if len(query) != 0:
            response.status = "error"
            response.detail = "user already exists"
            return response
        else:
            # 写入新用户的数据
            user = Database_auth_user_list(
                email=data.email,
                password=get_hashed_password(data.password),
                nick_name=data.nick_name,
            )
            return response
