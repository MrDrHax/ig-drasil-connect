from pydantic import BaseModel

class Summary(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        orm_mode = True