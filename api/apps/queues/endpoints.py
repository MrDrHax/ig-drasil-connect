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
        await queues_contacts_on_queue(token)  
        # await get_connected_users(token),
    ]

    graphs = [
        await queues_answer_time(token),
        await queues_contact_duration(token)  
        # await graph_example(),
        # await get_avg_contact_duration(token),
    ]

    toReturn = models.DashboardData(cards=cards, graphs=graphs)

    return toReturn

# list_queues

# @router.get("/queues/contacts-on-queue", tags=["cards"])
# async def queues_contacts_on_queue(token: Annotated[str, Depends(requireToken)]):
#     '''
#     Returns the answer time of the queues that will be displayed on a graph.
#     '''
#     availableQueues = ["Tickets Management", "Customize Assistance", "Event News", "Default Queue","Supervisor", "Callback"]

#     if not userType.isManager(token):
#         raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

#     client = boto3.client('connect')
#     queues = client.list_queues(
#         InstanceId = Config.INSTANCE_ID,
#     )

#     myQueues = []
#     myQueuesDic = {}
#     for queue in queues['QueueSummaryList']:
#         if queue['QueueType'] == "STANDARD":
#             if queue['Name'] in availableQueues:
#                 myQueues.append(queue)
#                 myQueuesDic[queue['Id']] = queue['Name']
#                 print(queue['Name'])
#                 print(queue['Id'])

#     queues_data = client.get_metric_data_v2(
#         # InstanceId = Config.INSTANCE_ID,
#         ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e',
#         StartTime = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 0),
#         EndTime = datetime.now(),
#         Interval = {
#             'TimeZone': 'UTC',
#             'IntervalPeriod': 'TOTAL',
#         },
#         Filters = [{
#             'FilterKey': 'QUEUE',
#             'FilterValues': [queue['Id'] for queue in myQueues],
#         }],
#         Groupings = ['QUEUE'],
#         Metrics = [
#             {
#                 'Name': 'CONTACTS_ABANDONED',
#                 'MetricFilters': [{
#                     'MetricFilterKey': 'INITIATION_METHOD',
#                     'MetricFilterValues': [
#                         'INBOUND',
#                     ]
#                 }]
#             }
#         ]
#     )

#     queue_series =[]
#     categories = []
#     # for queue in queues_data['MetricResults']:
#     #     queue_series.append(models.SeriesData(name = myQueuesDic[queue['Dimensions']['QUEUE']], 
#     #                                           data=[queue['Collections'][0]['Value']]))
#     #     categories.append(myQueuesDic[queue['Dimensions']['QUEUE']])


#     # cardFooter = models.CardFooter(
#     #     color = color,
#     #     value= str(count),
#     #     label="Available agents",
#     # )

#     # card = models.GenericCard(
#     #     id=1,
#     #     title="online agents",
#     #     value= str(users_data['ApproximateTotalCount']),
#     #     icon="HandRaisedIcon",
#     #     footer=cardFooter,
#     # )

#     return queues_data



@router.get("/queues/answer-time", tags=["cards"])
async def queues_answer_time(token: Annotated[str, Depends(requireToken)]) -> models.GenericGraph:
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
    myQueuesDic = {}
    for queue in queues['QueueSummaryList']:
        if queue['QueueType'] == "STANDARD":
            if queue['Name'] in availableQueues:
                myQueues.append(queue)
                myQueuesDic[queue['Id']] = queue['Name']

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
    categories = []
    for queue in queues_data['MetricResults']:
        queue_series.append(models.SeriesData(name = myQueuesDic[queue['Dimensions']['QUEUE']], 
                                              data=[queue['Collections'][0]['Value']]))
        categories.append(myQueuesDic[queue['Dimensions']['QUEUE']])


    queue_xaxis = models.XAxisData(
        categories = categories
    )

    queue_options = models.GraphOptions(
        colors = ["#3b82f6", "#f87171"],
        xaxis = queue_xaxis
    )

    queue_chart = models.ChartData(
        type = "bar",
        series = queue_series,
        options = queue_options
    )

    queue_graph = models.GenericGraph(
        title = "Queue Answer Time",
        description = "This graph shows the average time it takes for a call to be answered by queue.",
        footer = ("Updated at: " + str(datetime.now().hour) + ":" + str(datetime.now().minute)),
        chart = queue_chart
    )

    return queue_graph
    # return queues_data




@router.get("/queues/contact-duration", tags=["cards"])
async def queues_contact_duration(token: Annotated[str, Depends(requireToken)]) -> models.GenericGraph:
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
    myQueuesDic = {}
    for queue in queues['QueueSummaryList']:
        if queue['QueueType'] == "STANDARD":
            if queue['Name'] in availableQueues:
                myQueues.append(queue)
                myQueuesDic[queue['Id']] = queue['Name']

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
                'Name': 'AVG_CONTACT_DURATION'
            }
        ]
    )

    queue_series =[]
    categories = []
    for queue in queues_data['MetricResults']:
        queue_series.append(models.SeriesData(name = myQueuesDic[queue['Dimensions']['QUEUE']], 
                                              data=[queue['Collections'][0]['Value']]))
        categories.append(myQueuesDic[queue['Dimensions']['QUEUE']])


    queue_xaxis = models.XAxisData(
        categories = categories
    )

    queue_options = models.GraphOptions(
        colors = ["#3b82f6", "#f87171"],
        xaxis = queue_xaxis
    )

    queue_chart = models.ChartData(
        type = "bar",
        series = queue_series,
        options = queue_options
    )

    queue_graph = models.GenericGraph(
        title = "Queue averae contact duration",
        description = "This graph shows the average time it takes for a call to be accomplished by queue.",
        footer = ("Updated at: " + str(datetime.now().hour) + ":" + str(datetime.now().minute)),
        chart = queue_chart
    )

    return queue_graph

    # AGENT_ANSWER_RATE
    # AGENT_OCCUPANCY -> solo para: Routing Profile, Agent, Agent Hierarchy
    # AVG_CONTACT_DURATION, AVG_INTERACTION_TIME, AVG_HANDLE_TIME
    # AVG_QUEUE_ANSWER_TIME
    # CONTACTS_ABANDONED
    # CONTACTS_PUT_ON_HOLD
    # CONTACTS_QUEUED

    # MAX_QUEUED_TIME

