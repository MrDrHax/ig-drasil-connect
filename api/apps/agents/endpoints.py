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
    Returns the cards that will be displayed on the dashboard.
    '''
    cards = [
        await online_agents(token),
        await need_assistance_agents(token),
    ]

    graphs = [
        await queues_agent_answer_rate(token),
        await queues_agent_occupancy(),
    ]

    toReturn = models.DashboardData(cards=cards, graphs=graphs)

    return toReturn

# list_users
# describe_agent_status
# list_agent_statuses

@router.get("/get/connected/agents", tags=["cards"])
async def online_agents():

    response = await cachedData.get("online_agents")
    
    return response



@router.get("/get/need-assistance/agents", tags=["cards"])
async def need_assistance_agents():

    response = await cachedData.get("need_assistance_agents")

    return response


@router.get("/queues/agent-answer-rate", tags=["cards"])
async def queues_agent_answer_rate():
    
    response = await cachedData.get("queues_agent_answer_rate")

    return response


@router.get("/queues/agent-occupancy", tags=["cards"])
async def queues_agent_occupancy():
    
    response = await cachedData.get("queues_agent_occupancy")

    return response


# @router.get("/list/list-agent")
# async def list_agent():
    
#     client = boto3.client('connect')
#     resp = client.list_users(
#         InstanceId=Config.INSTANCE_ID

#     )

#     return resp

# AGENT_ANSWER_RATE
# AGENT_OCCUPANCY -> solo para: Routing Profile, Agent, Agent Hierarchy
# AVG_CONTACT_DURATION, AVG_INTERACTION_TIME, AVG_HANDLE_TIME
# AVG_QUEUE_ANSWER_TIME
# CONTACTS_ABANDONED
# CONTACTS_PUT_ON_HOLD
# CONTACTS_QUEUED

# MAX_QUEUED_TIME
