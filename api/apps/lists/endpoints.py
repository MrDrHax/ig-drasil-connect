from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from . import crud, models
from AAA.requireToken import requireToken
import AAA.userType as userType

import boto3
from config import Config

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

class QueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100, sortByDat: str | None = None, sortBy: str = 'asc'):
        self.q = q
        self.skip = skip
        self.limit = limit
        if not sortByDat or not sortBy:
            self.sortBy = None
        else:
            self.sortBy = (sortByDat, sortBy)


@router.get("/queues", tags=["queues"])
async def get_queues(qpams: Annotated[QueryParams, Depends()]) -> models.QueueDataList:
    '''
    Returns a list of all available queues.

    To see details, go to summary/queues/{queueID}
    '''

    return models.QueueDataList(pagination="1-4/4",
        data=[models.QueueDataListItem(queueID="a", name="Support", maxContacts=10, usage=5, enabled=True), 
            models.QueueDataListItem(queueID="b", name="Sales", maxContacts=10, usage=5, enabled=True), 
            models.QueueDataListItem(queueID="c", name="Final sale", maxContacts=10, usage=5, enabled=True), 
            models.QueueDataListItem(queueID="d", name="Advanced support", maxContacts=10, usage=5, enabled=True)])

@router.get("/reconnected", tags=["reconnected", "calls"])
async def get_reconnected_calls(qpams: Annotated[QueryParams, Depends()]) -> models.ListData:
    '''
    Returns a list of all calls that were reconnected within the last hour.

    To see details, go to summary/calls/{callID}
    '''

    return models.ListData(name="Reconnected calls", description="Calls that were reconnected within the last hour.", 
                           data=[models.ListItem(callID=1, name="John", agent="Ron (support)", started="2021-07-26T14:00:00", ended="2021-07-26T14:30:00", rating=4.5), 
                                 models.ListItem(callID=2, name="Jane", agent="Ron (support)", started="2021-07-26T14:00:00", ended=None, rating=4.5), 
                                 models.ListItem(callID=3, name="John", agent="Ron (support)", started="2021-07-26T14:00:00", ended="2021-07-26T14:30:00", rating=4.5)],
                           pagination="1-3/3")

@router.get("/calls", tags=["calls"])
async def get_calls(qpams: Annotated[QueryParams, Depends()]) -> models.ListData:
    '''
    Returns a list of all ongoing calls.

    To see details, go to summary/calls/{callID}
    '''

    return models.ListData(name="Ongoing calls", description="Calls that are currently ongoing.", 
                           data=[models.ListItem(callID=1, name="John", agent="Ron (support)", started="2021-07-26T14:00:00", ended=None, rating=4.5), 
                                 models.ListItem(callID=2, name="Jane", agent="Ron (support)", started="2021-07-26T14:00:00", ended=None, rating=4.5), 
                                 models.ListItem(callID=3, name="John", agent="No agent", started="2021-07-26T14:00:00", ended=None, rating=2.5)],
                           pagination="1-3/3")

@router.get("/angry", tags=["calls", "angry"])
async def get_angry_calls(qpams: Annotated[QueryParams, Depends()]) -> models.ListData:
    '''
    Returns a list of all calls that have clients angry, shouting or treating the operator badly.

    To see details, go to summary/calls/{callID}
    '''

    return models.ListData(name="Angry calls", description="Calls that were rated under 3.", 
                           data=[models.ListItem(callID=1, name="John", agent="Ron (support)", started="2021-07-26T14:00:00", ended="2021-07-26T14:30:00", rating=2.5), 
                                 models.ListItem(callID=2, name="Jane", agent="Ron (support)", started="2021-07-26T14:00:00", ended=None, rating=2.5), 
                                 models.ListItem(callID=3, name="John", agent="Ron (support)", started="2021-07-26T14:00:00", ended="2021-07-26T14:30:00", rating=2.5)],
                           pagination="1-3/3")

async def get_agent_name(Id: str) -> str:
    '''
    Returns the name of a given agent, from their Id

    Id: The identifier of the agent account

    Returns: The name of the agent
    '''
    client = boto3.client('connect')
    response = client.describe_user(
        InstanceId=Config.INSTANCE_ID,
        UserId=Id
    )
    return f"{response['User']['IdentityInfo']['FirstName']} {response['User']['IdentityInfo']['LastName']}"

def get_routing_profile_name(Id: str, routing_profile_list: list) -> str:
    '''
    Returns the name of a given routing profile, from their Id

    Id: The identifier of the routing profile

    Returns: The name of the routing profile
    '''
    for profile in routing_profile_list:
        if profile['Id'] == Id:
            return profile['Name']

@router.get("/agents", tags=["agents"])
async def get_agents(qpams: Annotated[QueryParams, Depends()], token: Annotated[str, Depends(requireToken)]) -> models.AgentsDataList:
    '''
    Returns a list of all available agents (even on break).

    To see details, go to summary/agents/{agentID}

    statuses: "connected", "disconnected", "on-call", "busy", "on-break"
    '''

    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    client = boto3.client('connect')

    # Get a list of all routing profiles
    response = client.list_routing_profiles(
        InstanceId=Config.INSTANCE_ID
    )

    routingProfiles = response['RoutingProfileSummaryList']

    # Get a list of the Arn for each routing profile
    routingProfilesArns = [profile['Arn'] for profile in routingProfiles]


    # Get info for all the routing profiles
    response = client.get_current_user_data(
        InstanceId=Config.INSTANCE_ID,
        Filters={
            'RoutingProfiles': routingProfilesArns
        }
    )

    try :
        list = response['UserDataList']
        parsed = [models.AgentsDataListItem(
                                  agentID=str(userData['User']['Id']), 
                                  name= await get_agent_name(userData['User']['Id']),
                                  queue= get_routing_profile_name(userData['RoutingProfile']['Id'], routingProfiles),
                                  status= userData['Status']['StatusName'], 
                                  requireHelp=userData['Status']['StatusName'] == "Needs Assistance", calls=5, rating=4.5) 
                                  for userData in list]
        
        return models.AgentsDataList(pagination="1-1/1", data=parsed)
        

    except Exception as e:
        print(e)
    
        if (qpams.skip != 0):
            return models.AgentsDataList(pagination="5-8/8",
            data=[models.AgentsDataListItem(agentID="adsfg", name="cheff", status="connected", calls=5, rating=4.5), 
                models.AgentsDataListItem(agentID="bbcvn", name="dude", status="connected", calls=5, rating=4.5), 
                models.AgentsDataListItem(agentID="cewrt", name="robert", status="connected", calls=5, rating=4.5), 
                models.AgentsDataListItem(agentID="dfghj", name="test", status="connected", calls=5, rating=4.5, requireHelp=True)])
        return models.AgentsDataList(pagination="1-4/8",
            data=[models.AgentsDataListItem(agentID="adsfg", name="Ron", status="connected", calls=5, rating=4.5), 
                models.AgentsDataListItem(agentID="bbcvn", name="Jane", status="connected", calls=5, rating=4.5), 
                models.AgentsDataListItem(agentID="cewrt", name="John", status="connected", calls=5, rating=4.5), 
                models.AgentsDataListItem(agentID="dfghj", name="Ron", status="connected", calls=5, rating=4.5, requireHelp=True)])

@router.get("/rerouted", tags=["calls"])
async def get_rerouted_calls(qpams: Annotated[QueryParams, Depends()]) -> models.ListData:
    '''
    Returns a list of all calls that have been rerouted more than 3 times.

    To see details, go to summary/calls/{callID}
    '''

    return models.ListData(name="Rerouted calls", description="Calls that have been rerouted more than 3 times.", 
                           data=[models.ListItem(callID=1, name="John", agent="Ron (support)", started="2021-07-26T14:00:00", ended="2021-07-26T14:30:00", rating=4.5), 
                                 models.ListItem(callID=2, name="Jane", agent="Ron (support)", started="2021-07-26T14:00:00", ended=None, rating=4.5), 
                                 models.ListItem(callID=3, name="John", agent="Ron (support)", started="2021-07-26T14:00:00", ended="2021-07-26T14:30:00", rating=4.5)],
                           pagination="1-3/3")