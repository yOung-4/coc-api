from fastapi import APIRouter, Depends
from common.roll import roll
from pydantic import BaseModel

router = APIRouter()
r = roll()


class char_info_base(BaseModel):
    STR: int
    CON: int
    SIZ: int
    DEX: int
    APP: int
    INT: int
    POW: int
    EDU: int
    LUC: int
