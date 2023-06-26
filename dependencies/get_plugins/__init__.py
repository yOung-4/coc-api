from dependencies.plugins.get_env import get_env
from dependencies.plugins.security import get_hashed_password
from pony import orm


def dependencies_get_env():
    return get_env


def dependencies_get_hashed_password():
    return get_hashed_password


def dependencies_get_db():
    return orm.db_session
