from fastapi import APIRouter, Depends,HTTPException
import requests
from typing import Annotated
from . import crud, models
from cache.cache_object import cachedData
import markdown
from AAA.requireToken import requireToken
import AAA.userType as userType
import re 
import json

import logging
logger = logging.getLogger(__name__)

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

@router.get("/AI/AgentPerformance")
async def read_agent_performance_summary(agent_id: str, token: Annotated[str, Depends(requireToken)] ) -> models.AgentPerformanceSummary:
    if not userType.testToken(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be logged in to access this.")
    res = await cachedData.get('fetchRecommendations', agent_id=agent_id)
    
    html_content = markdown.markdown(res).replace("\n", "")

    return models.AgentPerformanceSummary(agent_id=agent_id, content=html_content)

@router.get("/AI/AgentTranscript")
async def read_agent_transcript_summary(agent_id: str) -> models.AgentTranscriptSummary:
    res = await cachedData.get('getLatestAgentTranscript', agent_id=agent_id)

    data = json.loads(res)
    
    return models.AgentTranscriptSummary(agent_id=agent_id, content=str(data))

@router.get("/AI/AgentContact")
async def read_agent_contact_summary(agent_id: str) -> models.AgentTranscriptSummary:
    res = await cachedData.get('getLatestAgentContact', agent_id=agent_id)

    return models.AgentTranscriptSummary(agent_id=agent_id, content=str(res))
