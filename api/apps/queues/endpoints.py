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
                print(queue['Id'])
                print(queue['Name'])

    queues_data = client.get_metric_data_v2(
        # InstanceId = Config.INSTANCE_ID,
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e',
        StartTime = datetime.now() - timedelta(days=34),
        EndTime = datetime.now(),
        Interval = {
            'TimeZone': 'UTC',
            'IntervalPeriod': 'TOTAL',
        },
        Filters = [{
            'FilterKey': 'QUEUE',
            'FilterValues': [queue['Id'] for queue in myQueues],
        }],
        Groupings = ['QUEUE'],
        Metrics = [
            {
                'Name': 'AVG_QUEUE_ANSWER_TIME'
            }
        ]
    )

    queue_series =[]
    for queue in myQueues:
        queue_series.append(models.SeriesData(name=queue['Name'], data=[]))

    queue_series = models.SeriesData(name="Queue 1", data=[20,30,50,40,10])

    series_example = [models.SeriesData(name="Agent 1", data=[20,30,50,40,10]), models.SeriesData(name="Agent 2", data=[100, 120, 20, 50, 10])]

    xaxis_example = models.XAxisData(
        categories=["Jan", "Feb", "March", "Apr", "May"]
    )

    example_options = models.GraphOptions(
        colors=["#3b82f6", "#f87171"],
        xaxis=xaxis_example
    )

    example_chart = models.ChartData(
        type="line",
        series= series_example,
        options=example_options
    )

    example_graph = models.GenericGraph(
        title="Example Graph",
        description="Graph showing number of calls per month",
        footer="Updated 1st of June",
        chart = example_chart
    )

    # return example_graph


    return queues_data



    # AGENT_ANSWER_RATE
    # AGENT_OCCUPANCY -> solo para: Routing Profile, Agent, Agent Hierarchy
    # AVG_CONTACT_DURATION, AVG_INTERACTION_TIME, AVG_HANDLE_TIME
    # AVG_QUEUE_ANSWER_TIME
    # CONTACTS_ABANDONED
    # CONTACTS_PUT_ON_HOLD
    # CONTACTS_QUEUED

    # MAX_QUEUED_TIME
