from fastapi import APIRouter, Depends,HTTPException
import requests
from typing import Annotated
from . import crud, models
from apps.dashboard import models as dashboardModels
from cache.cache_object import cachedData
import markdown
from AAA.requireToken import requireToken
import AAA.userType as userType

from datetime import datetime

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
async def read_agent_performance_summary(agent_id: str, token: Annotated[str, Depends(requireToken)]) -> models.AgentPerformanceSummary:
    if not userType.testToken(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be logged in to access this.")

    res = await cachedData.get('fetchRecommendations', agent_id=agent_id)
    
    html_content = markdown.markdown(res).replace("\n", "")

    return models.AgentPerformanceSummary(agent_id=agent_id, content=html_content)

@router.get("/AgentRatings")
async def read_agent_ratings(agent_id: str, token: Annotated[str, Depends(requireToken)]) -> list[models.AgentRating]:
    """
    Returns a list of ratings for the agent.
    """
    if not userType.testToken(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be logged in to access this.")

    res = await cachedData.get('getListAgentRatings', agent_id=agent_id)

    return res


@router.get("/AgentContacts", tags=["contacts"])
async def read_agent_contacts(agent_id: str, token: Annotated[str, Depends(requireToken)]) -> list[dict]:
    """
    Returns a list of contacts for the agent.
    """
    if not userType.testToken(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be logged in to access this.")

    res = await cachedData.get('getAllAgentContact', agent_id=agent_id)

    return res

@router.get("/AgentRatingGraph", tags=["profile" ,"graph"] )
async def read_agent_rating_graph(agent_id: str, token: Annotated[str, Depends(requireToken)]) -> list[dashboardModels.GenericGraph]:
    """
    Returns a graph of ratings for the agent.
    """
    if not userType.testToken(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be logged in to access this.")

    list = await cachedData.get('getListAgentRatings', agent_id=agent_id)


    ratings = [ x.rating for x in list ]
    times = [ x.timestamp.strftime("%m-%d %H:%M") for x in list ]

    chart_info = dashboardModels.ChartData(type="line", series=[dashboardModels.SeriesData(name="Rating", data=ratings)], options=dashboardModels.GraphOptions(xaxis=dashboardModels.XAxisData(categories=times)))
    res = dashboardModels.GenericGraph(title="Agent Rating Graph", description="Graph showing agent rating through time", footer="Updated " + datetime.now().strftime("%m-%d @ %H:%M"), chart=chart_info)

    return [res]

@router.get("/AgentRatingAvg", tags=["profile"])
async def read_agent_rating(agent_id: str, token: Annotated[str, Depends(requireToken)]) -> list[float]:
    if not userType.testToken(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be logged in to access this.")

    list = await cachedData.get('getListAgentRatings', agent_id=agent_id)

    res = [0.0, 0.0]
    for rating in list:
        res[0] += rating.rating
        res[1] += 1

    # The first value is the avg of all the ratings and the second is the number of ratings
    res[0] = res[0] / res[1]

    return res