from fastapi import APIRouter
from . import crud, models

router = APIRouter(prefix="/summaries", tags=["summaries"])

@router.get("/")
async def read_summary(summary_id: int) -> models.Summary:
    return models.Summary(title="test", content="test", id=3)

