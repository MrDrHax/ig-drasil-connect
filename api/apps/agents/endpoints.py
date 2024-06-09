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
    Returns the cards that will be displayed on the agent dashboard.
    '''

    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    cards = [
        await online_agents(token),
        await need_assistance_agents(token),
    ]

    graphs = [
        # await graph_example(),
        # await get_avg_contact_duration(token),
        # await get_queues(token),  
    ]

    toReturn = models.DashboardData(cards=cards, graphs=graphs)

    return toReturn

@router.get("/get/connected/agents", tags=["cards"])
async def online_agents(token: Annotated[str, Depends(requireToken)]) -> models.GenericCard:
    '''
    Returns the number of people that are currently online.
    
    ''' 
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")


    client = boto3.client('connect')
    users = client.list_users(
        InstanceId=Config.INSTANCE_ID,
    )
    userList = []
    for user in users['UserSummaryList']:
        userList.append(user['Id'])

    users_data = client.get_current_user_data(
        InstanceId=Config.INSTANCE_ID,
        Filters={
            'Agents': userList
        }
    )

    count = 0
    for user in users_data['UserDataList']:
        if user['Status']['StatusName'] == "Available":
            count += 1

    if count <= 5:
        color = "text-red-500"
    else:
        color = "text-green-500"

    cardFooter = models.CardFooter(
        color = color,
        value= str(count),
        label="Available agents",
    )

    card = models.GenericCard(
        id=1,
        title="online agents",
        value= str(users_data['ApproximateTotalCount']),
        icon="HandRaisedIcon",
        footer=cardFooter,
    )

    return card

@router.get("/get/need-assistance/agents", tags=["cards"])
async def need_assistance_agents(token: Annotated[str, Depends(requireToken)]):
    '''
    Returns the number of people that need assistance and are currently online.
    
    ''' 
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")


    client = boto3.client('connect')
    users = client.list_users(
        InstanceId=Config.INSTANCE_ID,
    )
    userList = []
    for user in users['UserSummaryList']:
        userList.append(user['Id'])

    users_data = client.get_current_user_data(
        InstanceId=Config.INSTANCE_ID,
        Filters={
            'Agents': userList
        }
    )

    count = 0
    assistanceCount = 0
    for user in users_data['UserDataList']:
        if user['Status']['StatusName'] == "Needs Assistance":
            count += 1
            if datetime.now(user['Status']['StatusStartTimestamp'].tzinfo) - user['Status']['StatusStartTimestamp'] >= timedelta(minutes=5):
                assistanceCount += 1
                


    if count >= 3:
        color = "text-red-500"
    else:
        color = "text-green-500"

    cardFooter = models.CardFooter(
        color = color,
        value= str(assistanceCount),
        label="have passed over 5 minutes wating for assistance",
    )

    card = models.GenericCard(
        id=1,
        title="Agents that need assistance",
        value= str(count),
        icon="HandRaisedIcon",
        footer=cardFooter,
    )

    return card

@router.get("/list/list-agent-statuses")
async def list_agent_statuses():
    """
    Returns a list of all agent statuses.

    @return: list of agent statuses
    """

    resp = await cachedData.get('getListAgentStatuses')

    return resp
