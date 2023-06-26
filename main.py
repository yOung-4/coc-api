from fastapi import FastAPI
from api.Auth import SignUp


app = FastAPI()

app.include_router(SignUp.router, tags=["auth"])