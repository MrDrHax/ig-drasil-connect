from fastapi import APIRouter
from . import models, crud
from typing import List
from config import Config

import boto3

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

@router.get("/graph/usage", tags=["graph"])
async def get_usage_graph() -> models.UsageGraph:
    '''
    Returns a graph of what queues is being used and capacity of each queue.
    
    100 means the queue is full, 0 means the queue is empty.
    Anything over a 100 is considered an overflow. (waiting users)

    Will not consider the number of agents in break or disconnected.
    '''

    return models.UsageGraph(data=[20,30,50], labels=["1", "2", "3", "4", "5"])

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