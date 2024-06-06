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
    prefix="/queues", 
    tags=["queues"], 
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
        # await get_connected_users(token),
    ]

    graphs = [
        # await graph_example(),
        # await get_avg_contact_duration(token),
        # await get_queues(token),  
    ]

    toReturn = models.DashboardData(cards=cards, graphs=graphs)

    return toReturn

# list_queues

@router.get("/get/queues", tags=["cards"])
async def get_queues(token: Annotated[str, Depends(requireToken)]):
    '''
    Returns the queues that will be displayed on the dashboard.
    '''
    availableQueues = ["Tickets Management", "Customize Assistance", "Event News", "Default Queue","Supervisor", "Callback"]

    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    client = boto3.client('connect')
    queues = client.list_queues(
        InstanceId = Config.INSTANCE_ID,
    )

    myQueues = []
    for queue in queues['QueueSummaryList']:
        if queue['QueueType'] == "STANDARD":
            if queue['Name'] in availableQueues:
                myQueues.append(queue)

    queues_data = client.describe_queue(
        InstanceId = Config.INSTANCE_ID,
        QueueId = myQueues[0]['Id']
    )


    return queues_data