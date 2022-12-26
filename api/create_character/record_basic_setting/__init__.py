from fastapi import APIRouter, Depends, Form
from depends.token_log_in import get_current_user
from database import Character_Basic, session

router = APIRouter()
session = session()


@router.post('/ecord_basic_setting', tags=['create_character'])
def record_basic_character(
        current_user=Depends(get_current_user),
        character_name: str = Form(),
        age: int = Form(),
        gender: str = Form(),
        address: str = Form(),
        birthplace: str = Form()):
    new_character_basic = Character_Basic(
        user_id=current_user[0],
        character_name=character_name,
        age=age,
        gender=gender,
        address=address,
        birthplace=birthplace
    )
    session.add(new_character_basic)
    session.commit()
    return {'status code': 'record OK'}