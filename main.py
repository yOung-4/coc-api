from fastapi import FastAPI

from models.characters import new_character
from api.auth import login, sign_up

app = FastAPI()

app.include_router(new_character.router)
app.include_router(sign_up.router)
app.include_router(login.router)

@app.get("/")
async def root():
    return {"stutes": "OK"}