from fastapi import APIRouter, Depends
from typing import Annotated
from . import crud, models

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
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100, sortBy: tuple[str, str] | None = None):
        self.q = q
        self.skip = skip
        self.limit = limit
        self.sortBy = sortBy 

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

@router.get("/agents", tags=["agents"])
async def get_agents(qpams: Annotated[QueryParams, Depends()]) -> models.AgentsDataList:
    '''
    Returns a list of all available agents (even on break).

    To see details, go to summary/agents/{agentID}
    '''

    return models.AgentsDataList(pagination="1-4/4",
        data=[models.AgentsDataListItem(agentID="a", name="Ron", status="Available", calls=5, rating=4.5), 
            models.AgentsDataListItem(agentID="b", name="Jane", status="Available", calls=5, rating=4.5), 
            models.AgentsDataListItem(agentID="c", name="John", status="Available", calls=5, rating=4.5), 
            models.AgentsDataListItem(agentID="d", name="Ron", status="Available", calls=5, rating=4.5)])
