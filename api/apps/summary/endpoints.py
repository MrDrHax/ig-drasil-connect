from fastapi import APIRouter
from . import crud, models

router = APIRouter(
    prefix="/summaries", 
    tags=["summaries"], 
    responses = {
        200: {"description": "Success"},
        #202: {"description": "Accepted, request is being processed. Applies for connect requests that might take a while."},
        400: {"description": "Bad request, parameters are missing or invalid"},
        401: {"description": "Unauthorized. The request was not authorized."},
        404: {"description": "Not found"},
        500: {"description": "Internal server error, unknown error occurred."},
        503: {"description": "Service unavailable. Amazon Connect did not respond."},
    }
)

@router.get("/")
async def read_summary(summary_id: int) -> models.Summary:
    return models.Summary(title="test", content="test", id=3)
