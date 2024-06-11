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

@router.get("/reconnected", tags=["reconnected", "calls"])
async def get_reconnected_calls(qpams: Annotated[QueryParams, Depends()], token: Annotated[str, Depends(requireToken)]) -> models.ListData:
    '''
    Returns a list of all calls that were reconnected within the last hour.

    To see details, go to summary/calls/{callID}
    '''

    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    return models.ListData(name="Reconnected calls", description="Calls that were reconnected within the last hour.", 
                           data=[models.ListItem(callID=1, name="John", agent="Ron (support)", started="2021-07-26T14:00:00", ended="2021-07-26T14:30:00", rating=4.5), 
                                 models.ListItem(callID=2, name="Jane", agent="Ron (support)", started="2021-07-26T14:00:00", ended=None, rating=4.5), 
                                 models.ListItem(callID=3, name="John", agent="Ron (support)", started="2021-07-26T14:00:00", ended="2021-07-26T14:30:00", rating=4.5)],
                           pagination="1-3/3")

@router.get("/calls", tags=["calls"])
async def get_calls(qpams: Annotated[QueryParams, Depends()], token: Annotated[str, Depends(requireToken)]) -> models.ListData:
    '''
    Returns a list of all ongoing calls.

    To see details, go to summary/calls/{callID}
    '''

    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    return models.ListData(name="Ongoing calls", description="Calls that are currently ongoing.", 
                           data=[models.ListItem(callID=1, name="John", agent="Ron (support)", started="2021-07-26T14:00:00", ended=None, rating=4.5), 
                                 models.ListItem(callID=2, name="Jane", agent="Ron (support)", started="2021-07-26T14:00:00", ended=None, rating=4.5), 
                                 models.ListItem(callID=3, name="John", agent="No agent", started="2021-07-26T14:00:00", ended=None, rating=2.5)],
                           pagination="1-3/3")

@router.get("/angry", tags=["calls", "angry"])
async def get_angry_calls(qpams: Annotated[QueryParams, Depends()], token: Annotated[str, Depends(requireToken)]) -> models.ListData:
    '''
    Returns a list of all calls that have clients angry, shouting or treating the operator badly.

    To see details, go to summary/calls/{callID}
    '''

    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    return models.ListData(name="Angry calls", description="Calls that were rated under 3.", 
                           data=[models.ListItem(callID=1, name="John", agent="Ron (support)", started="2021-07-26T14:00:00", ended="2021-07-26T14:30:00", rating=2.5), 
                                 models.ListItem(callID=2, name="Jane", agent="Ron (support)", started="2021-07-26T14:00:00", ended=None, rating=2.5), 
                                 models.ListItem(callID=3, name="John", agent="Ron (support)", started="2021-07-26T14:00:00", ended="2021-07-26T14:30:00", rating=2.5)],
                           pagination="1-3/3")


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

@router.get("/rerouted", tags=["calls"])
async def get_rerouted_calls(qpams: Annotated[QueryParams, Depends()], token: Annotated[str, Depends(requireToken)]) -> models.ListData:
    '''
    Returns a list of all calls that have been rerouted more than 3 times.

    To see details, go to summary/calls/{callID}
    '''

    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    return models.ListData(name="Rerouted calls", description="Calls that have been rerouted more than 3 times.", 
                           data=[models.ListItem(callID=1, name="John", agent="Ron (support)", started="2021-07-26T14:00:00", ended="2021-07-26T14:30:00", rating=4.5), 
                                 models.ListItem(callID=2, name="Jane", agent="Ron (support)", started="2021-07-26T14:00:00", ended=None, rating=4.5), 
                                 models.ListItem(callID=3, name="John", agent="Ron (support)", started="2021-07-26T14:00:00", ended="2021-07-26T14:30:00", rating=4.5)],
                           pagination="1-3/3")