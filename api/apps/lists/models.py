from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class ListModel(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class ListBase(BaseModel):
    name: str

class ListCreate(ListBase):
    pass

class List(ListBase):
    id: int

    class Config:
        orm_mode = True