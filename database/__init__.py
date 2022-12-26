from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("postgresql://web:kokodayo@127.0.0.1:5432/api", future=True, echo=True)
session = sessionmaker(engine)

Base = declarative_base()


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    nick_name = Column(String, nullable=False)
    password = Column(String, nullable=False)


class Character_Basic(Base):
    __tablename__ = 'Character_Basic'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    # --------------------
    character_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=True)
    address = Column(String, nullable=True)
    birthplace = Column(String, nullable=True)


class Character_Ability(Base):
    __tablename__ = 'Character_Ability'
    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey('Character_Basic.id'))

# User.__table__.create(engine)
# Character_Basic.__table__.create(engine)
# Character_Ability.__table__.create(engine)
