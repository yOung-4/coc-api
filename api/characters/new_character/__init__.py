from fastapi import APIRouter, Depends
from common.roll import roll
from common.auth import get_current_user
from pydantic import BaseModel
from configs.database import db

router = APIRouter()
r = roll()
db_conn = db()

class char_info_base(BaseModel):
    STR: int = 0
    CON: int = 0
    SIZ: int = 0
    DEX: int = 0
    APP: int = 0
    INT: int = 0
    POW: int = 0
    EDU: int = 0
    LUC: int = 0


@router.post("/char/new-char/1", tags=['char'])
def new_char_1(char_info_base: char_info_base, current_user_uuid = Depends(get_current_user)):
    #检查存放角色卡的表是否存在：
    cur = db_conn.create()
    cur.execute("SELECT char_card_num FROM user_info WHERE uuid = (%S)", (current_user_uuid,))
    db_result = cur.fetchall()
    #不存在则新建：
    if db_result[0][0] == 0:
        table_name = 'char_card_'  + current_user_uuid
        cur.execute('''CREATE TABLE %s 
            (id smallserial, 
            STR smallint, 
            CON smallint, 
            SIZ smallint, 
            DEX smallint, 
            APP smallint, 
            INT smallint, 
            POW smallint, 
            EDU smallint, 
            LUC smallint, ''', 
            (table_name,))
    #开roll！
    char_info_base.STR = r.roll(repeat=3, ranging=6, plus=5)
    char_info_base.CON = r.roll(ranging=6, repeat=3, plus=5)
    char_info_base.SIZ = r.roll(ranging=6, repeat=2, plus=5)
    char_info_base.DEX = r.roll(ranging=6, repeat=3, plus=5)
    char_info_base.APP = r.roll(ranging=6, repeat=3, plus=5)
    char_info_base.INT = r.roll(ranging=6, repeat=2, plus=5)
    char_info_base.POW = r.roll(ranging=6, repeat=3, plus=5)
    char_info_base.EDU = r.roll(ranging=6, repeat=2, plus=5, add=6)
    char_info_base.LUC = r.roll(ranging=6, repeat=3, plus=5)
    #检测用户是新增一张卡还是更改正在编辑的卡：
    cur.execute('''SELECT char_card_cache FROM user_info WHERE uuid = (%s)''', (current_user_uuid,))
    db_result = cur.fetchall()
    #如果正在编辑，则修改最后一项记录：
    if db_result[0][0] == True:
        #获取ID
        cur.execute()
        cur.execute\
            ('''UPDATE %s SET STR=(%s), CON=(%s), SIZ=(%s), DEX=(%s), APP=(%s), INT=(%s), POW=(%s), EDU=(%s), LUC=(%s) WHERE id = (%s)''', 
                (table_name,
                char_info_base.STR, 
                char_info_base.CON, 
                char_info_base.SIZ, 
                char_info_base.DEX, 
                char_info_base.APP, 
                char_info_base.INT, 
                char_info_base.POW, 
                char_info_base.EDU, 
                char_info_base.LUC, )
            )
    #否则就新增一条记录
    else:
        cur.execute('''INSERT INTO %s (%s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
            (char_info_base.STR, 
            char_info_base.CON, 
            char_info_base.SIZ, 
            char_info_base.DEX, 
            char_info_base.APP, 
            char_info_base.INT, 
            char_info_base.POW, 
            char_info_base.EDU, 
            char_info_base.LUC, ))
    return char_info_base