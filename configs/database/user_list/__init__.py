from configs.database.connection import Base, engine
from sqlalchemy import Column, String
from pydantic import BaseModel


class user_list(Base):
    __tablename__ = 'user_list'

    id = Column(String, primary_key=True)
    email = Column(String)
    password = Column(String)


Base.metadata.create_all(engine)


class user_list_class(BaseModel):
    id: str
    email: str
    password: str

    class Config:
        orm_mode = True
