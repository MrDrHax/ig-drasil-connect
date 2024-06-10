from pydantic import BaseModel, Field
import datetime

import logging
logger = logging.getLogger(__name__)

class ListItem(BaseModel):
    callID: int = Field(0, description="The id of the item. Use this to get the summary", examples=[1, 2, 3])
    name: str = Field("No name", description="The name of the connected person. Only applies if authenticated", example="John")
    agent: str = Field("No agent", description="Agent that is taking the call.", example="Ron (support)")
    started: datetime.datetime = Field(datetime.datetime.now(), description="When the call was started. Use this to get ongoing time", example="2021-07-26T14:00:00")
    ended: datetime.datetime = Field(None, description="If not none, the call has finished", example="2021-07-26T14:30:00", allow_none=True)
    rating: float = Field(0, description="The rating of the call. Higher is better. Uses KPIs to try to approach how well it's going", example=4.5)

    def __getitem__(self, item):
        return getattr(self, item)

class ListData(BaseModel):
    name: str = Field("No name", description="The name of the list.", example="Reconnected calls")
    description: str = Field("No description", description="The description of the list.", example="Calls that were reconnected within the last hour.")
    data: list[ListItem] = Field([], 
                                 description="The data to be displayed in the list.", 
                                 example=[{"callID": 1, "name": "John", "agent": "Ron (support)", "started": "2021-07-26T14:00:00", "ended": "2021-07-26T14:30:00", "rating": 4.5}])
    pagination: str = Field("-", description="The pagination of the list. Format: min-max/total", example="0-100/200")

    def __getitem__(self, item):
        return getattr(self, item)

class QueueDataListItem(BaseModel):
    queueID: str = Field("0", description="The id of the item. Use this to get the summary", examples=["a", "b", "c"])
    name: str = Field("No name", description="The name of the queue.", example="Support")
    description: str = Field("No description", description="The description of the queue.", example="The queue for support.")
    maxContacts: int = Field(10, description="The max amount of contacts a queue can have before considered full.", example=10)
    usage: float = Field(0, description="The current usage of the queue. 100 means full, 0 means empty.", example=5)
    enabled: bool = Field(True, description="If the queue is enabled or not.", example=True)
    waiting: int = Field(0, description="The amount of clients waiting in the queue.", example=5)
    averageWaitTime: float = Field(0, description="The average wait time for the clients in the queue.", example=5)
    routingProfiles: list[str] = Field([], description="The list of routing profiles associated with the queue.", example=["a", "b", "c"])

    def __getitem__(self, item):
        return getattr(self, item)

class QueueDataList(BaseModel):
    pagination: str = Field("-", description="The pagination of the list. Format: min-max/total", example="0-100/200")
    data: list[QueueDataListItem] = Field([], description="The contents of the list.", example=[{"queueID": "a", "name": "Support", "maxContacts": 10, "usage": 5, "enabled": True}])

    def __getitem__(self, item):
        return getattr(self, item)

class AgentsDataListItem(BaseModel):
    agentID: str = Field("0", description="The id of the item. Use this to get the summary", examples=["a", "b", "c"])
    name: str = Field("No name", description="The name of the agent.", example="Ron")
    status: str = Field("No status", description="The current status of the agent.", example="Available")
    queue: str = Field("No routing profile", description="The queue the agent is currently in.", example="Support")
    requireHelp: bool = Field(False, description="If the agent requires help or not.", example=False)
    queueList: list[str] = Field([], description="The list of queues the agent is currently available in.", example=["Support", "Support 2"])

    def __getitem__(self, item):
        return getattr(self, item)

class AgentsDataList(BaseModel):
    pagination: str = Field("-", description="The pagination of the list. Format: min-max/total", example="0-100/200")
    data: list[AgentsDataListItem] = Field([], description="The contents of the list.", example=[{"agentID": "a", "name": "Ron", "status": "Available", "calls": 5, "rating": 4.5}])

    def __getitem__(self, item):
        return getattr(self, item)