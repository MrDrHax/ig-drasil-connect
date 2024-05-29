from fastapi import APIRouter, Depends, HTTPException
from . import models, crud
from typing import List
from config import Config
from typing import Annotated
from AAA.requireToken import requireToken
import AAA.userType as userType
from cache.cache_object import cachedData
from datetime import datetime , timedelta

import random

import boto3
from config import Config

import logging
logger = logging.getLogger(__name__)

Icons = ["UserGroupIcon", "UserCicleIcon", "ClockIcon", "ClockIcon", "StarIcon"]

router = APIRouter(
    prefix="/dashboard", 
    tags=["dashboard"], 
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
        await get_connected_users(token),
        await get_capacity(token),
        await get_average_call_time(token),
        await get_connected_agents(token)
    ]

    graphs = [
        await graph_example(),
        await get_avg_contact_duration()
    ]
    '''    
    await get_unfinished_calls_graph(token),
    await get_average_call_rating_graph(token),
    await get_queues_graph(token)
    '''

    toReturn = models.DashboardData(cards=cards, graphs=graphs)

    return toReturn

@router.get("/connected-users" , tags=["cards"])
async def get_connected_users(token: Annotated[str, Depends(requireToken)]) -> models.GenericCard:
    '''
    Returns the amount of connected users.
    '''
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")
    
    footer_info = models.CardFooter(color="text-green-500", value="+32", label="than today's average")

    return models.GenericCard(id=1, title="Connected users", value="80", icon="Book", color="red", footer=footer_info)
    
@router.get("/capacity", tags=["cards"])
async def get_capacity(token: Annotated[str, Depends(requireToken)]) -> models.GenericCard:
    '''
    Returns the capacity
    '''
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")
    
    footer_info = models.CardFooter(color="text-green-500", value="+30%", label="more expected in the next hour")
    
    return models.GenericCard(id=2, title="Percent of capacity", value="10%", icon="Book", color="yellow", footer=footer_info)

@router.get("/average_call_time", tags=["cards"])
async def get_average_call_time(token: Annotated[str, Depends(requireToken)]) -> models.GenericCard:
    '''
    Returns the average call time.
    '''
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")
    
    footer_info = models.CardFooter(color="text-red-500", value="+23s", label="more than expected")
    
    return models.GenericCard(id=3, title="Average call time", value="3m23s", icon="Clock", color="blue", footer=footer_info)

@router.get("/connected_agents", tags=["cards"])
async def get_connected_agents(token: Annotated[str, Depends(requireToken)]) -> models.GenericCard:
    '''
    Returns the amount of connected agents.
    '''
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")
    
    footer_info = models.CardFooter(color="text-green-500", value="4", label="Online")
    
    return models.GenericCard(id=1, title="Connected agents", value="10", icon="Star", color="gray", footer=footer_info)

@router.get("/graph/unfinished_calls", tags=["graph"])
async def get_unfinished_calls_graph(token: Annotated[str, Depends(requireToken)]) -> models.GenericGraph:
    
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    return models.GenericGraph(title="Unfinished Calls" ,data=[20,30,50,40,10], labels=["-1hr","-50m", "-30m", "-10m", "0m"], description="Graph showing unfinished calls", footer="Updated 2 min ago")

@router.get("/graph/average_call_rating", tags=["graph"])
async def get_average_call_rating_graph(token: Annotated[str, Depends(requireToken)]) -> models.GenericGraph:
    
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")
    
    return models.GenericGraph(title="Average Call Rating", data=[20,30,50,40,10], labels=["-1hr","-50m", "-30m", "-10m", "0m"], description="Graph showing average call rating", footer="Updated 2 min ago")

@router.get("/graph/queues", tags=["graph"])
async def get_queues_graph(token: Annotated[str, Depends(requireToken)]) -> models.GenericGraph:
    '''
    Returns a graph of what queues is being used and capacity of each queue.
    
    100 means the queue is full, 0 means the queue is empty.
    Anything over a 100 is considered an overflow. (waiting users)
    
    '''
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    return models.GenericGraph(data=[20,30,50,40,10], labels=["Starting call", "Queue", "Agent","Transfers", "Delivery"], description="Graph showing queue capacity", footer="Updated 2 min ago")

@router.get("/graph_example", tags=["data"])
async def graph_example() -> models.GenericGraph:
    '''
    Returns an example of a generic graph.
    '''

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

    return example_graph

@router.get("/queue_supervisors", tags=["data"])
async def get_queue_supervisors() -> List[models.QueueSupervisor]:
    '''
    Returns the queue supervisors.
    '''
    return [
        models.QueueSupervisor(id=1, name="Supervisor 1", calls=10, status="online", usage=10.0),
        models.QueueSupervisor(id=2, name="Supervisor 2", calls=20, status="offline", usage=20.0),
        models.QueueSupervisor(id=3, name="Supervisor 3", calls=30, status="online", usage=30.0)
    ]

# @router.get("/agent_visualisation", tags=["data"])
# async def get_agent_visualisation() -> List[models.AgentVisualisation]:
#     '''
#     Returns the agent visualisation.
#     '''
#     return [
#         models.AgentVisualisation(agent_name="John Doe", routing_profile="Routing profile 1", status="Available"),
#         models.AgentVisualisation(agent_name="Jane Doe", routing_profile="Routing profile 2", status="Busy"),
#         models.AgentVisualisation(agent_name="John Smith", routing_profile="Routing profile 3", status="Away")
#     ]    

# @router.get("/graph/usage", tags=["graph"])
# async def get_usage_graph() -> models.UsageGraph:
#     '''
#     Returns a graph of what queues is being used and capacity of each queue.
    
#     100 means the queue is full, 0 means the queue is empty.
#     Anything over a 100 is considered an overflow. (waiting users)

#     Will not consider the number of agents in break or disconnected.
#     '''

#     return models.UsageGraph(data=[20,30,50,40,10], labels=["1", "2", "3", "4", "5"])

# @router.get("/graph/connection_status", tags=["graph"])
# async def get_connection_status_graph() -> models.UsageGraph:
#     '''
#     Returns a pie graph of the connection status of the queues.

#     Sum will always be 100.
#     '''

#     return models.UsageGraph(data=[20,50,30], labels=["Starting call", "Queue", "Agent"])

# @router.get("/data/lex_users", tags=["data"])
# async def get_lex_users() -> int:
#     '''
#     Returns the number of users using the Lex service.
#     '''

#     return 5

# @router.get("/data/calls", tags=["data"])
# async def get_ongoing_call_data() -> models.OngoingCallData:
#     '''
#     Returns data about agents connected, and in breaks, to see how many agents are available for calls.
#     '''

#     return models.OngoingCallData(costumers=10, agents=5, agents_in_break=2, rating=5.5)

# @router.get("/data/reconnected", tags=["data"])
# async def get_reconnected_calls() -> int:
#     '''
#     Returns the number of ongoing calls that were reconnected.

#     To get the full list, go to /lists/reconnected
#     '''

#     return 5

# @router.get("/data/angry", tags=["data"])
# async def get_angry_calls() -> int:
#     '''
#     Returns the number of ongoing calls that have been flagged as having an angry client.

#     To get the full list, go to /lists/angry
#     '''

#     return 'a'


# @router.get("/data/rerouted", tags=["lists"])
# async def get_rerouted_calls() -> int:
#     '''
#     Returns the number of calls that have been rerouted more than 3 times.
#     '''

#     return 'a'








# -------------------------------------------------------------------------------------------------------------------
# ----------------------------------Aqui empiezan los no forzados----------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------

# ------------------------------ Funciona
@router.get("/list-users-data", response_model=List[dict])
async def list_users_data():
    """
    Description:
        Return a list of agents of an instance.
    
    Parameters:
        * InstanceId [REQUIRED][string]: id of the Amazon Connect instance.
        * NextToken [string]: id of the Amazon Connect instance.
        * MaxResults [integer]: id of the Amazon Connect instance. Default=100

    @return 
        List containing the agents of an instance.
    """
    
    

    client = boto3.client('connect')

    # Get info about the users of said instance
    response = client.list_users(
        InstanceId=Config.INSTANCE_ID,
    )

    return response['UserSummaryList']

# ---------------------------------------------------- Volver a checar (requiere numero de telefono)
@router.get("/get-current-metric-data")
async def check_agent_availability(queue_id: str):
    """
    Description:
        Real-time information of the call.
    Parameters:
        * InstanceId [REQUIRED][string]: id of the Amazon Connect instance.
        * Filters [REQUIRED][dictionary]:  
            - 

    Read the docs:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_current_metric_data.html#

    @return 
        Metrics about an on-going call.

        ex. queue_id = '18494127-588c-4497-8291-9dacaee44341'
    """    


    client = boto3.client('connect')

    # Get info for the first routing profile
    response = client.get_current_metric_data(
        InstanceId=Config.INSTANCE_ID,
        Filters={
            'Queues': [queue_id],

            'Channels': [
                'VOICE'
            ]
        },
        CurrentMetrics=[
        {
            'Name': 'AGENTS_ONLINE',
            'Unit': 'COUNT'
        },
        ]
    )

    return response['MetricResults']

    # data = cachedData.get("check_agent_availability_data")

    # return data
# -------------------------------------------------Needs review
# @router.get("/agent-status", response_model=List[dict])
# async def check_agent_availability():
#     """
#     Description:
#         Verifies the status of agents in Amazon Connect.
#         It can be one of four things:

#         * AVAILABLE: on-duty and not in call
#         * OFFLINE: not on-duty and disconnected
#         * BUSY: with an open thread or ongoing call
#         * NEEDS ASSISTANCE: needs help from supervisor

#     Parameters:
#         * InstanceId [REQUIRED][string]: amazon connect instance identified
#         * AgentStatusTypes [list]: The available agent status types
#         * PaginationConfig [dictionary]
#             * MaxItems [int]: total number of items to return
#             * PageSize [int]: the size of each page
        
#     Read the docs:
#     https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListAgentStatuses.html

#     @return 
#         List containing the availability status of agents. (Not yet known)
#     """

#     client = boto3.client('connect')
#     paginator = client.get_paginator('list_agent_statuses')

#     # Get info for the first routing profile
#     response_iterator = paginator.paginate(
#         InstanceId = Config.INSTANCE_ID,
#         AgentStatusTypes = [
#             'AVAILABLE','OFFLINE','BUSY','ON BREAK','NEEDS ASSISTANCE',
#         ])
    
#     return response_iterator

@router.get("/agent-profile", tags=["profile"])
async def get_agent_profile(id: str) -> models.AgentProfileData:
    '''
    Returns the profile of an agent.

    To get the full list, go to /lists/agents
    '''
    try:
        client = boto3.client('connect')
        response = client.describe_user(
            InstanceId=Config.INSTANCE_ID,
            UserId=id
        )


        FullName = f'{response["User"]["IdentityInfo"]["FirstName"]} {response["User"]["IdentityInfo"]["LastName"]}'
        Agent_email = response["User"]["Username"]

        try:
            Agent_mobile = response["User"]["IdentityInfo"]["Mobile"]
        except:
            Agent_mobile = "Unknown"

        # FullName, Agent_email, Agent_mobile = cachedData.get("agent_profile_data", id=id)

        # logger.info(f"{FullName}, {Agent_email}, {Agent_mobile}")

        return models.AgentProfileData(name=FullName, queue='Support', rating=4, email=Agent_email, mobile=Agent_mobile)

    except Exception as e:
        logger.error(f"Error in get_agent_profile: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# list_recommenders_cache = []

# @router.get("/list-recommenders", response_model=List[dict])
# async def list_recommenders():
#     try:
#         client = boto3.client('connect')
#         response = client.list_queues(
#             InstanceId='string',
#             MaxResults=10
#         )
        
#         return response
#     except Exception as e: 
#         print(e.with_traceback)
#         print(e)
        

@router.get("/call-summary")
async def call_summary():
    """
    Description:
        Returns a series of metrics of a call with a certain contact specified by id

    Parameters:
        * InstanceId [REQUIRED][string]: amazon connect instance identified
        * ContactId [REQUIRED][string]: identifier of the contact
        
    Read the docs:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/describe_contact.html

    @return 
        JSON with the information on the call
    """
    try:
        client = boto3.client('connect')
        response = client.describe_contact(
            InstanceId=Config.INSTANCE_ID,
            ContactId='string'
        )
        
        return response
    except Exception as e: 
        print(e.with_traceback)
        print(e)

@router.get("/agent-status", response_model=List[dict])
async def agent_status():
    
    '''
    Returns the agent status.
    
    '''
    
    client = boto3.client('connect')
    response = client.list_agent_statuses(
        InstanceId=Config.INSTANCE_ID
    )
    
    return response['AgentStatusSummaryList']    

@router.get("/queue-description")
async def queue_description(queue_id: str):
    client = boto3.client('connect')
    response = client.describe_queue(
        InstanceId=Config.INSTANCE_ID,
        QueueId=queue_id
    )
    
    return response['Queue']

@router.get("/routing-profiles", response_model=List[dict])
async def routing_profiles():
    

    client = boto3.client('connect')

    # Get a list of all routing profiles
    response = client.list_routing_profiles(
        InstanceId=Config.INSTANCE_ID
    )

    return response['RoutingProfileSummaryList']

@router.get("/describe-routing-profile")
async def describe_routing_profile(routing_profile_id: str):
    client = boto3.client('connect')
    response = client.describe_routing_profile(
        InstanceId=Config.INSTANCE_ID,
        RoutingProfileId=routing_profile_id
    )
    
    return response['RoutingProfile']


@router.get("/list-routing-profile-queues")
async def list_routing_profile_queues(routing_profile_id: str):
    client = boto3.client('connect')

    response = client.list_routing_profile_queues(
        InstanceId=Config.INSTANCE_ID,
        RoutingProfileId=routing_profile_id
    )['RoutingProfileQueueConfigSummaryList']
    
    return response


@router.get("/list-queues")
async def list_queues():
    client = boto3.client('connect')
    response = client.list_queues(
    InstanceId=Config.INSTANCE_ID,
    )

    return response


@router.get("/describe-contact")
async def describe_contact(contact_id: str):

    client = boto3.client('connect')
    response = client.describe_contact(
        InstanceId=Config.INSTANCE_ID,
        ContactId=contact_id
    )

    return response['Contact']

# 802dc0a071714366b20b7dd891929556
@router.get("/desciribe-user")
async def describe_user(user_id:str):

    client = boto3.client('connect')
    response = client.describe_user(
        InstanceId=Config.INSTANCE_ID,
        UserId= user_id
    )
    return response['User']


# @router.get("/get-transcript")
# async def get_transcript(Contacd_Id: str, Connection_Token: str):

#     client = boto3.client('connectparticipant')
#     response = client.get_transcript(
#         ContactId = Contacd_Id,
#         ConnectionToken = request.cookies['access_token'], # Requerimos este token de autenticación.
#     )
#     return response['User']


@router.get("/metric-data")
async def metric_data(queue_id:str):

    client = boto3.client('connect')
    response = client.get_metric_data(
        InstanceId=Config.INSTANCE_ID,
        StartTime=datetime(2024, 5, 25, 0),
        EndTime=datetime(2024, 5, 25, 16),
        Filters={
            'Queues': [
                queue_id
                ]
        },
        Groupings=[
            'QUEUE'
        ],
        HistoricalMetrics=[
            {
                'Name': 'INTERACTION_TIME',
            # 'Threshold': {
            #     'Comparison': 'LT',
            #     'ThresholdValue': 123.0
            # },
                'Statistic': 'AVG',
                'Unit': 'SECONDS'
            },
        ]
    )

    print(response)

    return response['MetricResults']

@router.get("/current-metric-data")
async def current_metric_data(queue_id:str):

    client = boto3.client('connect')
    response = client.get_current_metric_data(
        InstanceId=Config.INSTANCE_ID,
        Filters={
            'Queues': [
                queue_id
            ],
            'Channels': [
                'VOICE'
            ]
        },
        Groupings=['QUEUE'],
        CurrentMetrics=[
        {
            'Name': 'AGENTS_AVAILABLE',
            'Unit': 'COUNT'
        },
        ]
    )

    print(response)

    return response['MetricResults']


@router.get("/current-user-data")
async def get_current_user_data():

    client = boto3.client('connect')
    response = client.get_current_user_data(
        InstanceId=Config.INSTANCE_ID,
        Filters={
            'Agents': [
                '1c38eb16-8f2c-4c9a-b723-8f0621583179',
                '270a9b75-7c3d-40de-b524-25011c6aeeb8',
                '305376be-597e-4c30-8cc1-d0ceb88699fe',
                '35eb516c-0c56-45a2-ab53-b09a43f196c3',
                '50f98823-5278-47fb-8c1a-e56fa525404a',
                '51ec1227-4119-412e-b0e6-2e3bbc6ae1a4',
                '7688a303-17b8-4402-b03f-d7ab051bde4e',
                '7d6be46a-287b-48fc-8bdb-70655a978247',
                '83656f24-be8f-4cc6-aca9-c3bf5c42e21a',
                '8d6f58c4-d1f5-4024-9ab0-c57666dd791b',
                '94c89e21-3aac-44b5-8ffa-c898061fddfd',
                'a3f8c7e6-712c-4c13-a9ae-5ed13e1f6523',                
                'b2ba1a5d-6f46-40a5-aa24-6b5032bf79fd',
                'ba862485-c72a-4fb9-8f98-58415b19482b',
                'c6437a67-db38-49da-8188-778ac2f1f555',
                'cf1410c7-01e9-484a-971a-e481924ee68e',
                'd2eed6e2-7bef-4983-83c8-cfd359d8cdbd',
                'fb1b7cb4-2e81-4d16-a50e-9726de5cc15a'
            ],
        #    'ContactFilter': {
        #         'ContactStates': [
        #             'CONNECTED'
        #         ]
        #     },
        },
        # CurrentMetrics=[
        # {
        #     'Name': 'AGENTS_AVAILABLE',
        #     'Unit': 'COUNT'
        # },
        # ]
    )

    print(response)

    return response['UserDataList']


# -------------------------------------------------------------------------------------------------------------------
# ----------------------------------Aqui empiezan los fregones----------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------


@router.get("/get-online-users-data")
async def get_online_users_data():
    client = boto3.client('connect')
    users = client.list_users(
        InstanceId=Config.INSTANCE_ID,
    )
    userList = []
    for user in users['UserSummaryList']:
        userList.append(user['Id'])

    response = client.get_current_user_data(
        InstanceId=Config.INSTANCE_ID,
        Filters={
            'Agents': userList
        }
    )
    return response['UserDataList']


@router.get("/get-not-connected-users-data")
async def get_not_connected_users_data():
    client = boto3.client('connect')
    users = client.list_users(
        InstanceId=Config.INSTANCE_ID,
    )
    userList = []
    for user in users['UserSummaryList']:
        userList.append(user['Id'])

    response = client.get_current_user_data(
        InstanceId=Config.INSTANCE_ID,
        Filters={
            'Agents': userList
        }
    )

    for user in response['UserDataList']:
        if user['User']['Id'] in userList:
            userList.remove(user['User']['Id'])

    for i in userList:
        print(i)

    return userList

@router.get("/average-call-time-duration")
async def get_average_call_time_duration():
    
    routing_profile_list = await routing_profiles()
    client = boto3.client('connect')
    
    response = client.get_metric_data_v2(
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e' ,
        StartTime = datetime.today() - timedelta(days=30),
        EndTime = datetime.today(),
        Interval = {
            'TimeZone': 'UTC',
            'IntervalPeriod': 'DAY',
        },
        Filters = [
            {
            'FilterKey': 'ROUTING_PROFILE',
            'FilterValues' : [i['Id'] for i in routing_profile_list],  
            } 
        ],
        
        Metrics = [
            {
                'Name': 'AVG_CONTACT_DURATION',
            }
        ]
        
    
    )

    return response['MetricResults']

@router.get("/graph/get-avg-contact-duration")
async def get_avg_contact_duration()-> models.GenericGraph:
    
    '''
    Returns the average contact duration.
    
    ''' 
        
    client = boto3.client('connect')

    routing_profile_list = await routing_profiles()
    
    response = client.get_metric_data_v2(
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e' ,
        StartTime = datetime.today() - timedelta(days=30),
        EndTime = datetime.today(),
        Interval = {
            'TimeZone': 'UTC',
            'IntervalPeriod': 'DAY',
        },
        Filters = [
            {
            'FilterKey': 'ROUTING_PROFILE',
            # Here we need to pass a list of routing profiles that we get from another endpoint
            'FilterValues' : [i['Id'] for i in routing_profile_list],
            } 
        ],
        
        Metrics = [
            {
                'Name': 'AVG_CONTACT_DURATION',
            }
        ]
        
    
    )

    #We need to get the timestamps for the x axis
    timestamps = []

    #We need to get the data for the y axis points
    data = []

    for j in range(len(response['MetricResults'])):
        # Save the timestamps in a list
        timestamps.append(response['MetricResults'][j]['MetricInterval']['StartTime'].strftime('%Y-%m-%d'))
        # Save the data in a list when the name is AVG_CONTACT_DURATION
        data.append(response['MetricResults'][j]['Collections'][0]['Value']) 

    # Create the graph points
    series_example = [models.SeriesData(name=response['MetricResults'][0]['Collections'][0]['Metric']['Name'], data=data)]

    # Create the x axis labels
    xaxis_example = models.XAxisData(
        categories=timestamps
    )

    # Create the graph options
    example_options = models.GraphOptions(
        xaxis=xaxis_example
    )

    # Create the graph type
    example_chart = models.ChartData(
        type="line",
        series= series_example,
        options=example_options
    )

    # Create the graph
    example_graph = models.GenericGraph(
        title="Average Contact Duration",
        description="Graph showing average contact duration per day in seconds",
        footer="Updated " + datetime.today().strftime('%Y-%m-%d'),
        chart = example_chart
    )

    return example_graph
