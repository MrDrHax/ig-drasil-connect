from fastapi import APIRouter, Depends, HTTPException
from . import models, crud
from typing import List
from config import Config
from typing import Annotated
from AAA.requireToken import requireToken
import AAA.userType as userType
from cache.cache_object import cachedData
from datetime import datetime , timedelta, date

import random

import boto3
from config import Config

import logging
logger = logging.getLogger(__name__)

Icons = ["UserGroupIcon", "UserCicleIcon", "ClockIcon", "ClockIcon", "StarIcon"]

router = APIRouter(
    prefix="/agents", 
    tags=["agents"], 
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

@router.get("/cards", tags=["cards"])
async def get_cards(token: Annotated[str, Depends(requireToken)]) -> models.DashboardData:
    '''
    Returns the cards that will be displayed on the list of agents dashboard.
    '''

    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    cards = [
        await online_agents(token),
        await need_assistance_agents(token),
    ]

    graphs = [
        await queues_agent_answer_rate(token),
        await queues_agent_occupancy(token),
    ]

    toReturn = models.DashboardData(cards=cards, graphs=graphs)

    return toReturn

@router.get("/connected", tags=["cards"])

async def online_agents(token: Annotated[str, Depends(requireToken)]) -> models.GenericCard:
    '''
    Returns the number of people that are currently online.
    
    ''' 
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    response = await cachedData.get("online_agents")
    
    return response

@router.get("/need-assistance", tags=["cards"])
async def need_assistance_agents(token: Annotated[str, Depends(requireToken)]) -> models.GenericCard:
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    response = await cachedData.get("need_assistance_agents")
    
    return response

@router.get("/queues/answer-rate", tags=["graphs"])
async def queues_agent_answer_rate(token: Annotated[str, Depends(requireToken)]):
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    response = await cachedData.get("queues_agent_answer_rate")
    
    return response

@router.get("/queues/occupancy", tags=["graphs"])
async def queues_agent_occupancy(token: Annotated[str, Depends(requireToken)]):
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    response = await cachedData.get("queues_agent_occupancy")
    
    return response