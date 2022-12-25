from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("postgresql://web:kokodayo@127.0.0.1:5432/api", future=True, echo=False)
session = sessionmaker(engine)

Base = declarative_base()
# User.__table__.create(engine)


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    nick_name = Column(String)
    password = Column(String)
