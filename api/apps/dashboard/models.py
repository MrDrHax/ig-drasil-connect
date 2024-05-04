from pydantic import BaseModel, Field

class DashboardItem(BaseModel):
    id: int
    name: str
    value: float
    description: str = None

    class Config:
        orm_mode = True

class UsageGraph(BaseModel):
    data: list[float] = Field([], examples=[[20,30,50], [100, 120, 20]])
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