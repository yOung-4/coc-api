from ..connection import Base
from sqlalchemy import Column, String

class user_list(Base):
    __tablename__ = 'user_list'

    id = Column(String, mrimary_key=True)
    email = Column(String)
    password = Column(String)