from pydantic import BaseModel, Field

import logging
logger = logging.getLogger(__name__)

class TopCards(BaseModel):
    id: int = Field(0, examples=[1, 2, 3])
    name: str = Field("Card name", examples=["Card 1", "Card 2", "Card 3"])
    price: float = Field(0.0, examples=[10.0, 20.0, 30.0])
    description: str = Field("Card description", examples=["Card 1 description", "Card 2 description", "Card 3 description"]) 
    
class ConnectedUsers(BaseModel):
    id: int = Field(0, examples=[1, 2, 3])
    title: str = Field("Connected users", examples=["Connected users"])
    user_amount: int = Field(0, examples=[10, 20, 30])
    footer_data: int = Field(0, examples=[10, 20, 30])
    footer_txt: str = Field("That's today's average.", examples=["That's today's average."])  

class ConnectedAgents(BaseModel):
    id: int = Field(0, examples=[1, 2, 3])
    title: str = Field("Connected agents", examples=["Connected agents"])
    agent_amount: int = Field(0, examples=[10, 20, 30])
    footer_data: int = Field(0, examples=[10, 20, 30])
    footer_txt: str = Field("That's today's average.", examples=["That's today's average."])
    
class Capacity(BaseModel):
    title: str = Field("Capacity name", examples=["Capacity 1", "Capacity 2", "Capacity 3"])
    percentaje: float = Field(0.0, examples=[10.0, 20.0, 30.0])
    description: str = Field("Capacity description", examples=["Capacity 1 description", "Capacity 2 description", "Capacity 3 description"])  

class AverageCallTime(BaseModel):
    title: str = Field("Average call time", examples=["Average call time"])
    ''' The title of the card.'''
    average: float = Field(0.0, examples=[10.0, 20.0, 30.0])
    '''The average time of a call in seconds.'''
    above_average: float = Field(0.0, examples=[10.0, 20.0, 30.0])
    '''The footer text of the card.'''
    footer_txt: str = Field("+23s more than expected" , examples=["+23s more than expected", "+10s more than expected", "+5s more than expected"])


class UnfinishedCallsGraph(BaseModel):
    title: str = Field("Unfinished calls", examples=["Unfinished calls"])
    ''' The title of the graph.'''
    data: list[int] = Field([], examples=[[20,30,50,40,10], [100, 120, 20, 50, 10]])
    '''The data to be displayed in the graph.'''
    labels: list[str] = Field([], examples=[["Starting call", "Queue", "Agent"], ["Finance", "Support", "Sales"]])
    '''The labels for the data. Will be the same length as the data list.'''
    
class QueueSupervisor(BaseModel):
    id: int = Field(0, examples=[1, 2, 3])
    name: str = Field("Supervisor name", examples=["Supervisor 1", "Supervisor 2", "Supervisor 3"])
    calls: int = Field(0, examples=[10, 20, 30])
    status: str = Field("online", examples=["online", "offline"])
    usage: float = Field(0.0, examples=[10.0, 20.0, 30.0])
    '''The status of the queue supervisor. Can be either "online" or "offline".'''
    
class AgentVisualisation(BaseModel):
    connected_users: int = Field(0, examples=[10, 20, 30])
    '''How many users are currently connected to an agent.'''
    usage_level: float = Field(0.0, examples=[10.0, 20.0, 30.0])
    '''The usage level of the agent. 0 to 100.'''
    agent_name: str = Field("Agent name", examples=["Agent 1", "Agent 2", "Agent 3"])
    '''The name of the agent.'''
    queue: str = Field("Queue name", examples=["Queue 1", "Queue 2", "Queue 3"])
    '''The name of the queue the agent is connected to.'''
    status: str = Field("online", examples=["online", "offline"])
    '''The status of the agent. Can be either "online" or "offline".'''
    help: bool = Field(False, examples=[True, False])    
class DashboardItem(BaseModel):
    id: int
    name: str
    value: float
    description: str = None

    class Config:
        from_attributes = True

class UsageGraph(BaseModel):
    data: list[float] = Field([], examples=[[20,30,50,40,10], [100, 120, 20, 50, 10]])
    '''The data to be displayed in the graph.'''
    labels: list[str] = Field([], examples=[["Starting call", "Queue", "Agent"], ["Finance", "Support", "Sales"]])
    '''The labels for the data. Will be the same length as the data list.'''

class OngoingCallData(BaseModel):
    costumers: int = Field(0, examples=[10, 20, 30])
    '''How many costumers are currently connected to a call.'''
    agents: int = Field(0, examples=[5, 10, 15])
    '''How many agents are currently connected to a call.'''
    agents_in_break: int = Field(0, examples=[2, 4, 6])
    '''How many agents are currently taking a break.'''
    rating: float = Field(0, examples=[4.5, 3.5, 5.0])
    '''The average rating of a call. Range is 0 to 5'''

class AgentProfileData(BaseModel):
    name: str = Field(...)
    '''The name of the agent.'''
    queue: str = Field('Support', examples=['Support', 'Finance', 'Sales'])
    '''The queue the agent is in.'''
    rating: float = Field(0, examples=[4.5, 3.5, 5.0])
    '''The average rating of the agent. Range is 0 to 5'''
    email: str = Field(...)
    '''The email of the agent.'''  
    mobile: str = Field(...)
    '''The mobile of the agent.'''
