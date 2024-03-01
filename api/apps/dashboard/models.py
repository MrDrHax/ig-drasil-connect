from pydantic import BaseModel

class DashboardItem(BaseModel):
    id: int
    name: str
    value: float
    description: str = None

    class Config:
        orm_mode = True