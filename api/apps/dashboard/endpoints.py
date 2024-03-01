from fastapi import APIRouter
from . import models, crud

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/")
async def test() -> models.DashboardItem:
    return models.DashboardItem(name="test", description="test", value=1.0, id=1)
