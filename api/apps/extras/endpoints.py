from fastapi import APIRouter
from . import models, crud

router = APIRouter(prefix="/extras", tags=["extras"])

@router.get("/")
async def test(skip: int = 0, limit: int = 100) -> str:
    return f"Test has: skip={skip}, limit={limit}"
