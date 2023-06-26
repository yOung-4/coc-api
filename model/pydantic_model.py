from pydantic import BaseModel, BaseSettings


class env(BaseSettings):
    provider: str = "postgres"
    database_user: str
    password: str
    host: str = "127.0.0.1"
    database: str

    SECRET_KEY: str

    class Config:
        env_file = ".env"


class sign_up_request(BaseModel):
    email: str
    password: str
    nick_name: str
