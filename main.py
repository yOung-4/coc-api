from fastapi import FastAPI

from api import sign_up
from api import log_in

app = FastAPI()

app.include_router(sign_up.router)
app.include_router(log_in.router)
