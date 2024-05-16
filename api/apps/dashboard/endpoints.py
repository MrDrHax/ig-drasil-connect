from fastapi import APIRouter, Depends, HTTPException
from . import models, crud
from typing import List
from config import Config
from typing import Annotated
from AAA.requireToken import requireToken
import AAA.userType as userType
from cache.cache_object import cachedData

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
        await get_unfinished_calls_graph(token),
        await get_average_call_rating_graph(token),
        await get_queues_graph(token)
    ]

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

    return models.GenericCard(id=1, title="Connected users", value="80", icon=Icons, color="red", footer=footer_info)
    
@router.get("/capacity", tags=["cards"])
async def get_capacity(token: Annotated[str, Depends(requireToken)]) -> models.GenericCard:
    '''
    Returns the capacity
    '''
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")
    
    footer_info = models.CardFooter(color="text-green-500", value="+3", label="more expected in the next hour")
    
    return models.GenericCard(id=2, title="Capacity name", value="10%", icon=Icons, color="yellow", footer=footer_info)

@router.get("/average_call_time", tags=["cards"])
async def get_average_call_time(token: Annotated[str, Depends(requireToken)]) -> models.GenericCard:
    '''
    Returns the average call time.
    '''
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")
    
    footer_info = models.CardFooter(color="text-red-500", value="+23s", label="more than expected")
    
    return models.GenericCard(id=3, title="Average call time", value="10%", icon=Icons, color="blue", footer=footer_info)

@router.get("/connected_agents", tags=["cards"])
async def get_connected_agents(token: Annotated[str, Depends(requireToken)]) -> models.GenericCard:
    '''
    Returns the amount of connected agents.
    '''
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")
    
    footer_info = models.CardFooter(color="text-green-500", value="4", label="Online")
    
    return models.GenericCard(id=1, title="Connected agents", value="10", icon=Icons, color="gray", footer=footer_info)

@router.get("/graph/unfinished_calls", tags=["graph"])
async def get_unfinished_calls_graph(token: Annotated[str, Depends(requireToken)]) -> models.GenericGraph:
    
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    return models.GenericGraph(title="Unfinished Calls" ,data=[20,30,50,40,10], labels=["-1hr","-50m", "-30m", "-10m", "0m"], info="Graph showing unfinished calls", footer_txt="Updated 2 min ago")

@router.get("/graph/average_call_rating", tags=["graph"])
async def get_average_call_rating_graph(token: Annotated[str, Depends(requireToken)]) -> models.GenericGraph:
    
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")
    
    return models.GenericGraph(title="Average Call Rating", data=[20,30,50,40,10], labels=["-1hr","-50m", "-30m", "-10m", "0m"], info="Graph showing average call rating", footer_txt="Updated 2 min ago")

@router.get("/graph/queues", tags=["graph"])
async def get_queues_graph(token: Annotated[str, Depends(requireToken)]) -> models.GenericGraph:
    '''
    Returns a graph of what queues is being used and capacity of each queue.
    
    100 means the queue is full, 0 means the queue is empty.
    Anything over a 100 is considered an overflow. (waiting users)
    
    '''
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    return models.GenericGraph(data=[20,30,50,40,10], labels=["Starting call", "Queue", "Agent","Transfers", "Delivery"], info="Graph showing queue capacity", footer_txt="Updated 2 min ago")

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

@router.get("/agent_visualisation", tags=["data"])
async def get_agent_visualisation() -> List[models.AgentVisualisation]:
    '''
    Returns the agent visualisation.
    '''
    return [
        models.AgentVisualisation(agent_name="John Doe", routing_profile="Routing profile 1", status="Available"),
        models.AgentVisualisation(agent_name="Jane Doe", routing_profile="Routing profile 2", status="Busy"),
        models.AgentVisualisation(agent_name="John Smith", routing_profile="Routing profile 3", status="Away")
    ]    

@router.get("/graph/usage", tags=["graph"])
async def get_usage_graph() -> models.UsageGraph:
    '''
    Returns a graph of what queues is being used and capacity of each queue.
    
    100 means the queue is full, 0 means the queue is empty.
    Anything over a 100 is considered an overflow. (waiting users)

    Will not consider the number of agents in break or disconnected.
    '''

    return models.UsageGraph(data=[20,30,50,40,10], labels=["1", "2", "3", "4", "5"])

@router.get("/graph/connection_status", tags=["graph"])
async def get_connection_status_graph() -> models.UsageGraph:
    '''
    Returns a pie graph of the connection status of the queues.

    Sum will always be 100.
    '''

    return models.UsageGraph(data=[20,50,30], labels=["Starting call", "Queue", "Agent"])

@router.get("/data/lex_users", tags=["data"])
async def get_lex_users() -> int:
    '''
    Returns the number of users using the Lex service.
    '''

    return 5

@router.get("/data/calls", tags=["data"])
async def get_ongoing_call_data() -> models.OngoingCallData:
    '''
    Returns data about agents connected, and in breaks, to see how many agents are available for calls.
    '''

    return models.OngoingCallData(costumers=10, agents=5, agents_in_break=2, rating=5.5)

@router.get("/data/reconnected", tags=["data"])
async def get_reconnected_calls() -> int:
    '''
    Returns the number of ongoing calls that were reconnected.

    To get the full list, go to /lists/reconnected
    '''

    return 5

@router.get("/data/angry", tags=["data"])
async def get_angry_calls() -> int:
    '''
    Returns the number of ongoing calls that have been flagged as having an angry client.

    To get the full list, go to /lists/angry
    '''

    return 'a'


@router.get("/data/rerouted", tags=["lists"])
async def get_rerouted_calls() -> int:
    '''
    Returns the number of calls that have been rerouted more than 3 times.
    '''

    return 'a'

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


@router.get("/get-current-metric-data")
async def check_agent_availability() -> list[list[tuple]]:
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
    """    


    # client = boto3.client('connect')

    # # Get info for the first routing profile
    # response = client.get_current_metric_data(
    #     InstanceId=Config.INSTANCE_ID,
    #     Filters={
    #         'RoutingProfiles': [
    #             '69e4c000-1473-42aa-9596-2e99fbd890e7',
                
    #         ]
    #     },
    #     CurrentMetrics=[
    #     {
    #         'Name': 'AGENTS_ONLINE',
    #         'Unit': 'COUNT'
    #     },
    #     ]
    # )

    # return response['MetricResults']

    data = cachedData.get("check_agent_availability_data")

    return data

@router.get("/agent-status", response_model=List[dict])
async def check_agent_availability():
    """
    Description:
        Verifies the status of agents in Amazon Connect.
        It can be one of four things:

        * AVAILABLE: on-duty and not in call
        * OFFLINE: not on-duty and disconnected
        * BUSY: with an open thread or ongoing call
        * NEEDS ASSISTANCE: needs help from supervisor

    Parameters:
        * InstanceId [REQUIRED][string]: amazon connect instance identified
        * AgentStatusTypes [list]: The available agent status types
        * PaginationConfig [dictionary]
            * MaxItems [int]: total number of items to return
            * PageSize [int]: the size of each page
        
    Read the docs:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListAgentStatuses.html

    @return 
        List containing the availability status of agents. (Not yet known)
    """

    client = boto3.client('connect')
    paginator = client.get_paginator('list_agent_statuses')

    # Get info for the first routing profile
    response_iterator = paginator.paginate(
        InstanceId = Config.INSTANCE_ID,
        AgentStatusTypes = [
            'AVAILABLE','OFFLINE','BUSY','ON BREAK','NEEDS ASSISTANCE',
        ])
    
    return response_iterator

@router.get("/agent-profile", tags=["profile"])
async def get_agent_profile(id: str) -> models.AgentProfileData:
    '''
    Returns the profile of an agent.

    To get the full list, go to /lists/agents
    '''
    try:
        # client = boto3.client('connect')
        # response = client.describe_user(
        #     InstanceId=Config.INSTANCE_ID,
        #     UserId=id
        # )


        # FullName = f'{response["User"]["IdentityInfo"]["FirstName"]} {response["User"]["IdentityInfo"]["LastName"]}'
        # Agent_email = response["User"]["Username"]

        # try:
        #     Agent_mobile = response["User"]["IdentityInfo"]["Mobile"]
        # except:
        #     Agent_mobile = "Unknown"

        FullName, Agent_email, Agent_mobile = cachedData.get("agent_profile_data", id=id)

        logger.info(f"{FullName}, {Agent_email}, {Agent_mobile}")

        return models.AgentProfileData(name=FullName, queue='Support', rating=4, email=Agent_email, mobile=Agent_mobile)

    except Exception as e:
        logger.error(f"Error in get_agent_profile: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

list_recommenders_cache = []

@router.get("/list-recommenders", response_model=List[dict])
async def list_recommenders():
    try:
        client = boto3.client('connect')
        response = client.list_queues(
            InstanceId='string',
            MaxResults=10
        )
        
        return response
    except Exception as e: 
        print(e.with_traceback)
        print(e)
        

