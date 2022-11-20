from fastapi import FastAPI

from api.characters import new_character
from api.auth import login, sign_up

from common.auth import get_current_user
from common.roll import roll


app = FastAPI()

app.include_router(sign_up.router)
app.include_router(login.router)
app.include_router(new_character.router)

@app.get("/")
async def root():
    return {"stutes": "OK"}
