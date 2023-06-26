from fastapi import APIRouter, HTTPException, Depends
from model.pydantic_model import sign_up_request
from model.database_model import Database_sign_up_request
from pony import orm
from passlib.context import CryptContext
from dependencies.get_plugins import dependencies_get_db, dependencies_get_hashed_password

router = APIRouter()


@router.put("/auth/sign-up/")
async def sign_up(
        data: sign_up_request,
        db_conn: orm.Database = Depends(dependencies_get_db),
        get_hashed_password: CryptContext.hash = Depends(dependencies_get_hashed_password),
):
    with db_conn:
        query = orm.select(
            query for query in Database_sign_up_request if query.email == data.email
        )
        if len(query) != 0:
            raise HTTPException(status_code=400, detail="wrong email")
        else:
            user = Database_sign_up_request(
                email=data.email,
                password=get_hashed_password(data.password),
                nick_name=data.nick_name,
            )
            return {"message": "user_created",}