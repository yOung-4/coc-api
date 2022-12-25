from fastapi import FastAPI

from api.auth import log_in, sign_up
from api.create_character import record_basic_setting

app = FastAPI()

@app.post('/')
def status():
    return {'server status': 'OK'}


app.include_router(sign_up.router)
app.include_router(log_in.router)
app.include_router(record_basic_setting.router)
