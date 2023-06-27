from pydantic import BaseModel, BaseSettings
from typing import Union


# 环境变量模型
class env(BaseSettings):
    # 数据库环境变量
    provider: str = "postgres"
    database_user: str
    password: str
    host: str = "127.0.0.1"
    database: str
    port: str = "5432"

    # token与md5参数
    secret_key: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


# 请求体模型
class sign_up_request(BaseModel):
    email: str
    password: str
    nick_name: str


# 响应体模型
class general_response_model(BaseModel):
    status: str = "success"
    detail: Union[str, None] = None


class Token(BaseModel):
    access_token: str
    token_type: str
