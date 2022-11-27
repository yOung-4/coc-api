# 外部库导入
from fastapi import FastAPI

# 导入api模型
from api.characters import new_character
from api.auth import login, sign_up

# 导入内部模型
from common.auth import get_current_user
from common.roll import roll

app = FastAPI()


@app.get("/")
async def root():
    return {"stutes": "OK"}
