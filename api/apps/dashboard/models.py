from pydantic import BaseModel, Field

import logging
logger = logging.getLogger(__name__)

class CardFooter(BaseModel):
    color: str = Field("text-green-500", examples=["text-green-500", "text-gray-500", "text-red-500"])
    value: str = Field("0.0", examples=['10.0', '20.0', '30.0'])
    label: str = Field("minutes ago", examples=["minutes ago", "hours ago", "days ago"])

class GenericCard(BaseModel):
    id: int = Field(0, examples=[1, 2, 3])
    title: str = Field("Card name", examples=["Card 1", "Card 2", "Card 3"])
    value: str = Field("0.0", examples=['10.0', '20.0', '30.0'])
    icon: str = Field("Arrow", examples=["arrow"], description="The icon that will get added")
    color: str = Field("purple", examples=["black", "green"], description="The color of the icon")
    footer: CardFooter

class SeriesData(BaseModel):
    name: str = Field("Series 1", examples=["Series 1", "Series 2", "Series 3"])
    ''' The name of the series on the chart. '''
    data: list[float] = Field([], examples=[[20,30,50,40,10], [100, 120, 20, 50, 10]])
    ''' The data to be displayed in the series. '''

class XAxisData(BaseModel):
    categories: list[str] = Field([], examples=[["sales","delivery"], ["transfers", "agents", "queue"]])
    ''' The categories to be displayed on the x-axis. Has to be of the same length as the lenght of the series. '''

class GraphOptions(BaseModel):
    xaxis: XAxisData
    ''' The x-axis to be displayed in the chart. '''

class ChartData(BaseModel):
    type: str = Field("line", examples=["line", "bar"])
    ''' The type of chart.'''
    series: list[SeriesData]
    ''' The series to be displayed in the chart. '''
    options: GraphOptions
    ''' The options to be displayed in the chart. '''

class OcupacyCard(BaseModel):
    color: str 
    icon: str
    title: str
    value: int
    footer: dict[str, str] = Field({}, examples={"color": "text-green-500","value":"+3%", "label": "minutes ago"})
      

class GenericGraph(BaseModel):
    title: str = Field("Queues", examples=["Queues"])
    ''' The title of the graph.'''
    description: str = Field("Graph showing queue capacity", examples=["Graph showing queue capacity"])
    '''The info of the graph.'''
    footer: str = Field("Updated 2 min ago", examples=["Updated 2 min ago", "Updated 5 min ago", "Updated 10 min ago"])
    """The footer of the graph of when it was last updated."""
    chart: ChartData
    '''The chart to be displayed in the graph. '''
   
class DashboardData(BaseModel):
    cards: list[GenericCard] 
    graphs: list[GenericGraph]

'''
PREVIOUS EXAMPLES DISCONNECTED FROM THE FRONTEND

IGNORE THIS SECTION
'''

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

class QueuesGraph(BaseModel):
    title: str = Field("Queues", examples=["Queues"])
    ''' The title of the graph.'''
    data: list[int] = Field([], examples=[[20,30,50,40,10], [100, 120, 20, 50, 10]])
    '''The data to be displayed in the graph.'''
    labels: list[str] = Field([], examples=[["Starting call", "Queue", "Agent","Transfers", "Delivery"], ["Finance", "Support", "Sales","Transfers", "Delivery"]])
    '''The labels for the data. Will be the same length as the data list.'''
    info: str = Field("Graph showing queue capacity", examples=["Graph showing queue capacity"])
    '''The info of the graph.'''
    footer_txt: str = Field("Updated 2 min ago", examples=["Updated 2 min ago", "Updated 5 min ago", "Updated 10 min ago"])

class UnfinishedCallsGraph(BaseModel):
    title: str = Field("Unfinished calls", examples=["Unfinished calls"])
    ''' The title of the graph.'''
    data: list[int] = Field([], examples=[[20,30,50,40,10], [100, 120, 20, 50, 10]])
    '''The data to be displayed in the graph.'''
    labels: list[str] = Field([], examples=[["-1hr","-50m", "-30m", "-10m", "0m"], ["-1hr","-50m", "-30m", "-10m", "0m"]])
    '''The labels for the data. Will be the same length as the data list.'''
    info: str = Field("Graph showing unfinished calls", examples=["Graph showing unfinished calls"])
    '''The info of the graph.'''
    footer: str = Field("Updated 2 min ago", examples=["Updated 2 min ago", "Updated 5 min ago", "Updated 10 min ago"]) 
    
class AverageCallRating(BaseModel):
    title: str = Field("Average call rating", examples=["Average call rating"])
    ''' The title of the card.'''
    id: int = Field(0, examples=[1, 2, 3])
    '''The id of the info.'''
    Rating: int = Field([], examples=[50, 20, 90, 70, 100])
    '''The average rating of a call. Range is 0 to 100'''
    KPI: list[int]= Field([], examples=[50, 20, 90, 70, 100])
    '''The KPI of the card. Range is 0 to 100'''
    labels: list[str] = Field([], examples=[["-1hr","-50m", "-30m", "-10m", "0m"], ["-1hr","-50m", "-30m", "-10m", "0m"]])
    '''The labels for the data. Will be the same length as the data list.'''
    info: str = Field("Graph showing average call rating + important KPIs", examples=["Graph showing average call rating + important KPIs"])
    '''The info of the graph.'''
    footer: str = Field("Updated 2 min ago", examples=["Updated 2 min ago", "Updated 5 min ago", "Updated 10 min ago"])    
class QueueSupervisor(BaseModel):
    id: int = Field(0, examples=[1, 2, 3])
    name: str = Field("Supervisor name", examples=["Supervisor 1", "Supervisor 2", "Supervisor 3"])
    calls: int = Field(0, examples=[10, 20, 30])
    status: str = Field("online", examples=["online", "offline"])
    usage: float = Field(0.0, examples=[10.0, 20.0, 30.0])
    '''The status of the queue supervisor. Can be either "online" or "offline".'''
    
class AgentVisualisation(BaseModel):
    agent_name: str = Field("Agent name", examples=["John Doe", "Jane Doe", "John Smith"])
    '''The name of the agent.'''
    routing_profile: str = Field("Routing profile", examples=["Routing profile 1", "Routing profile 2", "Routing profile 3"])
    '''The routing profile of the agent.'''
    status: str = Field("Available", examples=["Available", "Busy", "Away"])
    '''The status of the agent. Can be either "Available", "Busy" or "Away".'''
    needs_help: bool = Field(True, examples=[True, False])
    '''If the agent needs help or not.'''
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
    name: str = Field('John Doe', examples=['John Doe', 'Jane Doe', 'John Smith'])
    '''The name of the agent.'''
    queue: str = Field('Support', examples=['Support', 'Finance', 'Sales'])
    '''The queue the agent is in.'''
    rating: float = Field(0, examples=[4.5, 3.5, 5.0])
    '''The average rating of the agent. Range is 0 to 5'''
    email: str = Field(...)
    '''The email of the agent.'''  
    mobile: str = Field(...)
    '''The mobile of the agent.'''
    roles: list[str] = Field([], examples=["Agent", "Supervisor", "Queue Supervisor"])
    '''The roles of the agent.'''


class LastContactCard(BaseModel):
    title: str = Field("Last contact", examples=["Last contact"])
    ''' The title of the card.'''
    last_contact: str = Field("2 minutes ago", examples=["2 minutes ago", "5 minutes ago", "10 minutes ago"])
    '''The last contact of the agent.'''
    footer_txt: str = Field("That's today's average.", examples=["That's today's average."])
    '''The footer text of the card.'''

class GenericAlert(BaseModel):
    Text: str = Field("Alert text", examples=["Alert text"])
    TextRecommendation: str = Field("Alert recommendation", examples=["Alert recommendation"])
    color: str = Field("red", examples=["red", "green", "yellow"])

