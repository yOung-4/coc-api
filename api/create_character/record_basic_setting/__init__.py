from fastapi import APIRouter, Depends
from depends.token_log_in import get_current_user

router = APIRouter()


@router.post('/ecord_basic_setting', tags=['create_character'])
def record_basic_character(current_user=Depends(get_current_user)):
    pass
