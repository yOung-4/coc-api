from dependencies.plugins.security import get_hashed_password, verify_password, create_access_token
from pony import orm
from model.pydantic_model import env


def dependencies_get_env() -> env:
    return env()


def dependencies_get_hashed_password() -> get_hashed_password:
    return get_hashed_password


def dependencies_verify_password() -> verify_password:
    return verify_password


def dependencies_create_access_token() -> create_access_token:
    return create_access_token


def dependencies_get_db() -> orm.db_session:
    return orm.db_session
