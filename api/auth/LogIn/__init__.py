from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from model.pydantic_model import general_response_model
from model.database_model import Database_auth_user_list
from dependencies.plugins.security import verify_password, create_access_token
from dependencies.get_plugins import dependencies_get_db, dependencies_verify_password, dependencies_create_access_token

from pony import orm

router = APIRouter()


@router.put("/token",)
def log_in(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db_conn: orm.Database = Depends(dependencies_get_db),
        verify_pwd: verify_password = Depends(dependencies_verify_password),
        create_token: create_access_token = Depends(dependencies_create_access_token()),
        response: general_response_model = Depends(general_response_model),
):
    with db_conn:
        query = orm.select(
            query for query in Database_auth_user_list if query.email == form_data.username
        )
        if len(query) == 0:
            response.status = "error"
            response.detail = "wrong password or username"
            return response
        if not verify_pwd(form_data.password, query.password):
            return response
        token = create_token(data={"sub", form_data.username})
        return token
