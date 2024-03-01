from fastapi import APIRouter
from . import crud, models

router = APIRouter(prefix="/lists", tags=["lists"])

@router.get("/")
async def read_list(list_id: int) -> models.List:
    return models.List(name="test", id=3)
    