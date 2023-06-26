from functools import lru_cache
from model.pydantic_model import env


@lru_cache()
def get_env():
    return env()