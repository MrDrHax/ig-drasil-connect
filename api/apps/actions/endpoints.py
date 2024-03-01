from fastapi import APIRouter
from . import models

router = APIRouter(prefix="/actions", tags=["actions"])

@router.get("/")
async def test() -> models.Action:
    """Test endpoint for actions."""
    return models.Action(name="test", description="test")