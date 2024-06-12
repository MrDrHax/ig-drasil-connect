from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from . import crud, models
from AAA.requireToken import requireToken
import AAA.userType as userType

from tools.lazySquirrel import LazySquirrel
from tools.querryParams import QueryParams

import boto3
from config import Config
from cache.cache_object import cachedData

import logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/lists", 
    tags=["lists"], 
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


@router.get("/queues", tags=["queues"])
async def get_queues(qpams: Annotated[QueryParams, Depends()], token: Annotated[str, Depends(requireToken)]) -> models.QueueDataList:
    '''
    Returns a list of all available queues.

    To see details, go to summary/queues/{queueID}
    '''

    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    data = await cachedData.get("get_queues_data")

    pagination, data = qpams.apply(data)

    return models.QueueDataList(pagination=pagination,
                                data=data)

@router.get("/agents", tags=["agents"])
async def get_agents(qpams: Annotated[QueryParams, Depends()], token: Annotated[str, Depends(requireToken)]) -> models.AgentsDataList:
    '''
    Returns a list of all available agents (even on break).

    To see details, go to summary/agents/{agentID}

    statuses: "connected", "disconnected", "on-call", "busy", "on-break"
    '''

    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    data = await cachedData.get("routing_profiles_data")

    pagination, data = qpams.apply(data)

    return models.AgentsDataList(pagination=pagination, data=data)

@router.get("/statuses", tags=["agents"])
async def get_statuses(token: Annotated[str, Depends(requireToken)]) -> list[dict]:
    """
    Returns all available statuses as a list of strings.
    """

    if not userType.isManager(token) and not userType.isAgent(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager or an agent to access this resource.")

    data = await cachedData.get("list_statuses")

    return data