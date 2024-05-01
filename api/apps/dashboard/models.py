from pydantic import BaseModel, Field

class TopCards(BaseModel):
    id: int = Field(0, examples=[1, 2, 3])
    name: str = Field("Card name", examples=["Card 1", "Card 2", "Card 3"])
    price: float = Field(0.0, examples=[10.0, 20.0, 30.0])
    description: str = Field("Card description", examples=["Card 1 description", "Card 2 description", "Card 3 description"]) 

class AverageCallTime(BaseModel):
    title: str = Field("Average call time", examples=["Average call time"])
    ''' The title of the card.'''
    average: float = Field(0.0, examples=[10.0, 20.0, 30.0])
    '''The average time of a call in seconds.'''
    above_average: float = Field(0.0, examples=[10.0, 20.0, 30.0])


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
        orm_mode = True

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