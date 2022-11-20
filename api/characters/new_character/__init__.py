from fastapi import APIRouter
import psycopg2
from models.gaming.roll import roll

router = APIRouter()

r = roll

#生成基本角色数据，不写入数据库
@router.get("/characters/new-character/new-basic-attributes", tags=['new-characte'])
def new():
    basic_attributes = \
        {'DEX': r.roll(ranging=6, repeat=3, plus=5),
        'APP': r.roll(ranging=6, repeat=3, plus=5),
        'INT': r.roll(ranging=6, repeat=2, plus=5),
        'POW': r.roll(ranging=6, repeat=3, plus=5),
        'EDU': r.roll(ranging=6, repeat=2, plus=6, add=6),
        'LUC': r.roll(ranging=6, repeat=3, plus=5)
        }
    return basic_attributes


