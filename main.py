from fastapi import FastAPI

from api import sign_up

app = FastAPI()

app.include_router(sign_up.router)
