from sqlalchemy import Column, Integer, String
# from db import Base

from pydantic import BaseModel

class Action(BaseModel):
    name: str
    description: str