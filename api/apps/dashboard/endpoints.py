from fastapi import APIRouter
from . import models, crud
from typing import List
from config import Config

import boto3
from config import Config

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

@router.get("/cards", tags=["cards"] , response_model=List[models.TopCards])
async def get_cards() -> models.TopCards:
    '''
    Returns the cards that will be displayed on the dashboard.
    '''
    cards = [
        models.TopCards(id=1, name="Card 1", price=10.0, description="Card 1 description"),
        models.TopCards(id=2, name="Card 2", price=20.0, description="Card 2 description"),
        models.TopCards(id=3, name="Card 3", price=30.0, description="Card 3 description")
    ]
    return cards

@router.get("/connected-users" , tags=["users"], response_model=List[models.ConnectedUsers])
async def get_connected_users() -> List[models.ConnectedUsers]:
    '''
    Returns the amount of connected users.
    '''
    return models.ConnectedUsers(id=1, title="Connected users", user_amount=10, footer_data=10, footer_txt="That's today's average.")
        
    
@router.get("/capacity", tags=["cards"])
async def get_capacity() -> models.Capacity:
    '''
    Returns the capacity
    '''
    return models.Capacity(title="Capacity name", percentaje=10.0, description="Capacity description")

@router.get("/average_call_time", tags=["cards"])
async def get_average_call_time() -> models.AverageCallTime:
    '''
    Returns the average call time.
    '''
    return models.AverageCallTime(title="Average call time", average=10.0, above_average=20.0, footer_txt="+23s more than expected")

@router.get("/connected_agents", tags=["cards"])
async def get_connected_agents() -> models.ConnectedAgents:
    '''
    Returns the amount of connected agents.
    '''
    return models.ConnectedAgents(id=1, title="Connected agents", agent_amount=10, footer_data=10, footer_txt="That's today's average.")

@router.get("/graph/unfinished_calls", tags=["graph"])
async def get_unfinished_calls_graph() -> models.UnfinishedCallsGraph:
    

    return models.UnfinishedCallsGraph(data=[20,30,50,40,10], labels=["Starting call", "Queue", "Agent"])

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
        models.AgentVisualisation(connected_users=10, usage_level=10.0, agent_name="Agent 1", queue="Queue 1", status="online", help=True),
        models.AgentVisualisation(connected_users=20, usage_level=20.0, agent_name="Agent 2", queue="Queue 2", status="offline", help=False),
        models.AgentVisualisation(connected_users=30, usage_level=30.0, agent_name="Agent 3", queue="Queue 3", status="online", help=True)
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


@router.get("/get-current-metric-data", response_model=List[dict])
async def check_agent_availability():
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


    client = boto3.client('connect')

    # Get info for the first routing profile
    response = client.get_current_metric_data(
        InstanceId=Config.INSTANCE_ID,
        Filters={
            'RoutingProfiles': [
                '69e4c000-1473-42aa-9596-2e99fbd890e7',
                
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
        ],
        PaginationConfig = {
            'MaxItems': 50,
            'PageSize': 50
        })
    
    return response_iterator

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

        print(FullName, Agent_email, Agent_mobile)


        return models.AgentProfileData(name=FullName, queue='Support', rating=4, email=Agent_email, mobile=Agent_mobile)

    except Exception as e:
        print("Error:")
        return models.AgentProfileData(name=id, queue='Unknown', rating=0, email='Unknown', mobile='Unknown')


# @router.get("/list-recommenders", response_model=List[dict])
# async def list_recommenders():
#     client = boto3.client('connect')
#     paginator = client.get_paginator('list_recommenders')
#     response_iterator = paginator.paginate(
#         datasetGroupArn = Config.DATASET_GROUP_ARN,
#         PaginationConfig = {
#             'MaxItems': 50,
#             'PageSize': 50
#         })
#     return response_iterator
        

