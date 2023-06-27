from fastapi import FastAPI
from api.auth import SignUp


app = FastAPI()

app.include_router(SignUp.router, tags=["auth"],)
