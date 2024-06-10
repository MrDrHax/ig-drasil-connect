from fastapi import APIRouter, Depends, HTTPException
from . import models, crud
from typing import List
from config import Config
from typing import Annotated
from AAA.requireToken import requireToken
import AAA.userType as userType
from cache.cache_object import cachedData
from datetime import datetime , timedelta, date
from tools.lazySquirrel import LazySquirrel

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
        # await get_connected_users(token),
        await get_capacity(token),
        await get_average_call_time(token),
        await get_connected_users(token),
        # await get_avg_handle_time(),
        await get_abandonment_rate(token),
        # await get_avg_holds(token),
    ]

    graphs = [
        await graph_example(),
        await get_avg_contact_duration(token),
        await get_queues(token),  
    ]

    toReturn = models.DashboardData(cards=cards, graphs=graphs)

    return toReturn

@router.get("/agent_cards", tags=["agent_view"])
async def get_agent_cards(token: Annotated[str, Depends(requireToken)], agent_id: str) -> models.DashboardData:
    '''
    Returns the cards that will be displayed on the agent dashboard.
    '''
    cards = [
        await get_avg_holds(token, agent_id),
        await get_People_to_answer(token),
        await get_capacity_agent(token, agent_id),
        await get_agent_rating(agent_id, token),
    ]

    graphs = [
    ]

    toReturn = models.DashboardData(cards=cards, graphs=graphs)

    return toReturn

@router.get("/graph_example", tags=["data"])
async def graph_example() -> models.GenericGraph:
    '''
    Returns an example of a generic graph.
    '''


    series_example = [models.SeriesData(name="Agent 1", data=[20,30,50,40,10]), models.SeriesData(name="Agent 2", data=[100, 120, 20, 50, 10])]

    xaxis_example = models.XAxisData(
        categories=["Jan", "Feb", "March", "Apr", "May"]
    )

    example_options = models.GraphOptions(
        colors=["#3b82f6", "#f87171"],
        xaxis=xaxis_example
    )

    example_chart = models.ChartData(
        type="line",
        series= series_example,
        options=example_options
    )

    example_graph = models.GenericGraph(
        title="Example Graph",
        description="Graph showing number of calls per month",
        footer="Updated 1st of June",
        chart = example_chart
    )

    return example_graph



@router.get("/list-queues")
async def list_queues():

    response =await cachedData.get("list_queue")

    return response

@router.get("/routing-profiles", response_model=List[dict])
async def routing_profiles():
    
    response = await cachedData.get("list_routing_profile")

    return response

@router.get("/get-online-users-data")
async def get_online_users_data():

    client = boto3.client('connect')
    users = client.list_users(
        InstanceId=Config.INSTANCE_ID,
    )
    userList = []
    for user in users['UserSummaryList']:
        userList.append(user['Id'])

    response = client.get_current_user_data(
        InstanceId=Config.INSTANCE_ID,
        Filters={
            'Agents': userList
        }
    )
    return response['UserDataList']

@router.get("/get-not-connected-users-data")
async def get_not_connected_users_data():

    client = boto3.client('connect')
    users = client.list_users(
        InstanceId=Config.INSTANCE_ID,
    )
    userList = []
    for user in users['UserSummaryList']:
        userList.append(user['Id'])

    response = client.get_current_user_data(
        InstanceId=Config.INSTANCE_ID,
        Filters={
            'Agents': userList
        }
    )

    for user in response['UserDataList']:
        if user['User']['Id'] in userList:
            userList.remove(user['User']['Id'])

    for i in userList:
        print(i)

    return userList


@router.get("/average-call-time-duration")
async def get_average_call_time(token: Annotated[str, Depends(requireToken)])->models.GenericCard:
    
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    routing_profile_list = await cachedData.get("list_routing_profile")
    client = boto3.client('connect')
    
    response = client.get_metric_data_v2(
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e' ,
        StartTime = datetime.today() - timedelta(days=30),
        EndTime = datetime.today(),
        Interval = {
            'TimeZone': 'UTC',
            'IntervalPeriod': 'DAY',
        },
        Filters = [
            {
            'FilterKey': 'ROUTING_PROFILE',
            'FilterValues' : [i['Id'] for i in routing_profile_list],  
            } 
        ],
        
        Metrics = [
            {
                'Name': 'AVG_CONTACT_DURATION',
            }
        ]
        
    
    )

    data=response['MetricResults'][0]['Collections'][0]['Value']

    extra = data/60 - 3

    cardFooter = models.CardFooter(
        color = "text-green-500" if extra < 3 else "text-red-500",
        value = "{p:.2f}".format(p=extra) + " minutes",
        label = ("less than max" if extra < 3 else "more than recommended") + ". The average duratino of a contact in minutes this month. Calls should be less than 3 minutes."
    )

    card = models.GenericCard(
        id=1,
        title="Average Call Time",
        value="{p:.2f}".format(p=data/60) + "m",
        icon="ClockIcon",
        footer=cardFooter,
        color="blue"
    )

    return card

@router.get("/graph/get-avg-contact-duration")
async def get_avg_contact_duration(token: Annotated[str, Depends(requireToken)])-> models.GenericGraph:
    
    '''
    Returns the average contact duration.
    
    ''' 
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    client = boto3.client('connect')

    routing_profile_list = await cachedData.get("list_routing_profile")
    
    response = client.get_metric_data_v2(
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e' ,
        StartTime = datetime.today() - timedelta(days=30),
        EndTime = datetime.today(),
        Interval = {
            'TimeZone': 'UTC',
            'IntervalPeriod': 'DAY',
        },
        Filters = [
            {
            'FilterKey': 'ROUTING_PROFILE',
            # Here we need to pass a list of routing profiles that we get from another endpoint
            'FilterValues' : [i['Id'] for i in routing_profile_list],
            } 
        ],
        
        Metrics = [
            {
                'Name': 'AVG_CONTACT_DURATION'
            },
            {
                'Name': 'ABANDONMENT_RATE'
            }
        ]
        
    
    )

    #We need to get the timestamps for the x axis
    timestamps = []

    #We need to get the data for the y axis points
    data = []

    for j in range(len(response['MetricResults'])):
        # Save the timestamps in a list
        timestamps.append(response['MetricResults'][j]['MetricInterval']['StartTime'].strftime('%Y-%m-%d'))
        # Save the data in a list when the name is AVG_CONTACT_DURATION
        data.append(response['MetricResults'][j]['Collections'][0]['Value']) 

    # Create the graph points
    series_example = [models.SeriesData(name=response['MetricResults'][0]['Collections'][0]['Metric']['Name'], data=data)]

    # Create the x axis labels
    xaxis_example = models.XAxisData(
        categories=timestamps
    )

    # Create the graph options
    example_options = models.GraphOptions(
        xaxis=xaxis_example
    )

    # Create the graph type
    example_chart = models.ChartData(
        type="line",
        series= series_example,
        options=example_options
    )

    # Create the graph
    example_graph = models.GenericGraph(
        title="Average Contact Duration",
        description="Graph showing average contact duration per day in seconds",
        footer="Updated " + datetime.today().strftime('%Y-%m-%d'),
        chart = example_chart
    )

    return example_graph


@router.get("/connected/users" , tags=["cards"])
async def get_connected_users(token: Annotated[str, Depends(requireToken)]) -> models.GenericCard:
    '''
    Returns the amount of connected agents.
    '''
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    data = await cachedData.get('routing_profiles_data')

    totalAgents = len(data)
    agentsInCall = len(LazySquirrel(data).filter_by('status', 'on call').get())
    agentsWhoNeedHelp = len(LazySquirrel(data).filter_by('status', 'needs assistance').get())
    
    footer_info = models.CardFooter(
        color = "text-red-500" if agentsWhoNeedHelp > 0 else "text-green-500", 
        value= f"{agentsWhoNeedHelp} agents", 
        label= "need help. Get more details on the agents tab.")
    
    card= models.GenericCard(
        id=1,
        title="Agents in call.",
        value=f'{agentsInCall} out of {totalAgents} connected agents',
        icon="UserIcon",
        footer=footer_info,
        color="pink",
    )
    return card


@router.get("/cards/capacity", tags=["cards"])
async def get_capacity(token: Annotated[str, Depends(requireToken)]) -> models.GenericCard:
    '''
    Returns the capacity
    '''
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")
    
    client = boto3.client('connect')

    routing_profile_list = await cachedData.get("list_routing_profile") 
    
    response = client.get_metric_data_v2(
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e' ,
        StartTime = datetime.today()-timedelta(days=1),
        EndTime = datetime.today(),
        Filters = [
            {
            'FilterKey': 'ROUTING_PROFILE',
            'FilterValues' : [i['Id'] for i in routing_profile_list],  
            } 
        ], 
        Metrics = [
            {
                'Name': 'AGENT_OCCUPANCY',
            }
        ]
    )

    response2 = client.get_metric_data_v2(
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e' ,
        StartTime = datetime.today() - timedelta(days=30),
        EndTime = datetime.today(),
        Interval = {
            'TimeZone': 'UTC',
            'IntervalPeriod': 'TOTAL',
        },
        Filters = [
            {
            'FilterKey': 'ROUTING_PROFILE',
            'FilterValues' : [i['Id'] for i in routing_profile_list],  
            } 
        ], 
        Metrics = [
            {
                'Name': 'AGENT_OCCUPANCY',
            }
        ]
    )

    datares1 = []
    for i in response['MetricResults']:
        for n in i['Collections']:
            datares1.append(n['Value'])
            print(datares1)
    
    datares2 = []
    for i in response2['MetricResults']:
        for n in i['Collections']:
            datares2.append(n['Value'])
            print(datares2)


    comp = datares1[0]-datares2[0]

    # dat

    cardFooter = models.CardFooter(
        color = "text-red-500" if comp > 0 else "text-green-500",
        value = "{:.2f}s".format(comp),
        label = ("more than last month" if comp > 0 else "less than last month") + ". The handle times should be less than 3 seconds. Handle time is the time it takes for an agent to take a call from when it first rings."
    )
    
    card = models.GenericCard(
        id = 1,
        title = "Average Handle Time",
        value =  "{:.2f}s".format(datares1[0]),
        icon = "UserIcon",
        footer = cardFooter,
        warning = datares1[0] > 3,
        color = "orange"
    )

    return card

@router.get("/cards/abandonment-rate", tags=["cards"])
async def get_abandonment_rate(token: Annotated[str, Depends(requireToken)]) -> models.GenericCard:

    # TODO fix this hot trash

    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")
    
    #routing_profile_list = await routing_profiles()
    client = boto3.client('connect')

    queues_list = await cachedData.get("list_queue")

    queues_id_list = []    
    for i in queues_list['QueueSummaryList']:
        if i['QueueType'] == 'STANDARD':
            queues_id_list.append(i['Id'])
    
    response = client.get_metric_data_v2(
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e' ,
        StartTime = datetime.today() - timedelta(days=30),
        EndTime = datetime.today(),
        Interval = {
            'TimeZone': 'UTC',
            'IntervalPeriod': 'TOTAL',
        },
        Filters = [
            {
            'FilterKey': 'QUEUE',
            'FilterValues' : queues_id_list,  
            } 
        ],
        Groupings=['QUEUE'],
        Metrics = [
            {
                'Name': 'ABANDONMENT_RATE',
            }
        ]
    )

    card_values = [i['Collections'][0]['Value'] for i in response['MetricResults']]
    card_value = sum(card_values) / len(card_values)

    # print(card_value)

    if (card_value > 80):
        footerColor = "text-red-500"
        footerSpecialText = f'{card_value - 80:.2f}%'
        footerDesc = 'more than the max recommended rate.'
    elif (card_value > 50):
        footerColor = "text-orange-500"
        footerSpecialText = f'{card_value - 50:.2f}%'
        footerDesc = 'more than the recommended rate.'
    else:
        footerColor = "text-green-500"
        footerSpecialText = f'{0}%'
        footerDesc = 'more than the max recommended rate.'

    cardFooter = models.CardFooter(
        color=footerColor,
        value=footerSpecialText,
        label=footerDesc + " The abandonment rate is the amount of calls that where ended by the user before having contact with an agent.",
    )

    card = models.GenericCard(
        id=1,
        title="Abandonment rate",
        value="{:.2f}%".format(card_value),
        icon="PhoneXMarkIcon",
        footer=cardFooter,
    )

    return card

@router.get("/graph/get-queues")
async def get_queues(token: Annotated[str, Depends(requireToken)]) -> models.GenericGraph:
    
    '''
    Returns the number of people in each queue
    
    ''' 
    client = boto3.client('connect')   

    queues_raw = await cachedData.get("list_queue")

    queues_list = []    
    
    for i in queues_raw['QueueSummaryList']:
        if i['QueueType'] == 'STANDARD':
            queues_list.append([i['Id'], i['Name']])

    response = client.get_current_metric_data(
        InstanceId=Config.INSTANCE_ID,
        Filters = {
            'Queues' : [i[0] for i in queues_list],
        },
        Groupings=['QUEUE',],
        CurrentMetrics = [
            {
                'Name': 'CONTACTS_IN_QUEUE', 
                'Unit': 'COUNT'
            }
        ],
    )

    data = []

    for j in response['MetricResults']:
        data.append(j['Collections'][0]['Value']) 
    
    series_example = [models.SeriesData(name=response['MetricResults'][0]['Collections'][0]['Metric']['Name'], data=data)]

    # Create the x axis labels
    xaxis_example = models.XAxisData(
        categories=[i[1] for i in queues_list]
    )

    # Create the graph options
    example_options = models.GraphOptions(
        xaxis=xaxis_example
    )

    # Create the graph type
    example_chart = models.ChartData(
        type="bar",
        series= series_example,
        options=example_options
    )

    # Create the graph
    example_graph = models.GenericGraph(
        title="Queues",
        description="Graph shows capacity the all queues",
        footer="Updated " + datetime.today().strftime('%Y-%m-%d') ,
        chart = example_chart
    )

    return example_graph   


# aqui va parte del agente hasta que funcione el dashboard agent


@router.get("/agent/avg-holds", tags=["agent"])
async def get_avg_holds(token: Annotated[str, Depends(requireToken)],agent_id:str)-> models.GenericCard:
    '''
    The total count of cases existing in a given domain. 
    '''

    if not userType.isAgent(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")
    client = boto3.client('connect')

    StartTime =  datetime((date.today() - timedelta(days=31)).year,
                          (date.today() - timedelta(days=31)).month, 1)
                                   
    EndTime =  datetime((date.today() - timedelta(days=31)).year, 
                                (date.today() - timedelta(days=31)).month, 
                                (datetime(date.today().year, date.today().month, 1) - timedelta(days=1)).day,
                                23, 59, 59)
    
    queues_list = await cachedData.get("list_queue")

    queues_id_list = []    
    for i in queues_list['QueueSummaryList']:
        if i['QueueType'] == 'STANDARD':
            queues_id_list.append(i['Id'])    
    
    today_res = client.get_metric_data_v2(
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e' ,
        StartTime = datetime(datetime.now().year, datetime.now().month, datetime.now().day),
        EndTime = datetime.now(),
        Interval = {
            'TimeZone': 'UTC',
            'IntervalPeriod': 'DAY',
        },
        Filters = [
            {
            'FilterKey': 'AGENT',
            'FilterValues' : [agent_id],  
            } 
        ], 
        Metrics = [
            {
                'Name': 'AVG_HOLDS',
            }
        ]
    )

    past_month_res = client.get_metric_data_v2(
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e' ,
        StartTime = StartTime,
        EndTime = EndTime,
        Interval = {
            'TimeZone': 'UTC',
            'IntervalPeriod': 'DAY',
        },
        Filters = [
            {
            'FilterKey': 'AGENT',
            'FilterValues' : [agent_id],  
            } 
        ], 
        Metrics = [
            {
                'Name': 'AVG_HOLDS',
            }
        ]
    )

    today_data = []
    for i in today_res['MetricResults']:
        for n in i['Collections']:
            today_data.append(n['Value'])

    past_month_data = []
    for i in past_month_res['MetricResults']:
        for n in i['Collections']:
            past_month_data.append(n['Value'])


    if len(today_data) == 0 or len(past_month_data) == 0:
        #Return an empty card in case of no data
        return models.GenericCard(
            id=1,
            title="Average Holds",
            value="0",
            icon="HandRaisedIcon",
            footer= models.CardFooter(
                color="text-red-500",
                value="0",
                label="The average number of times a voice contact was put on hold ",
            )
        )

    cardFooter = models.CardFooter(
        
        color="text-red-500" if today_data[0] <= past_month_data[0] else "text-green-500",
        value=(str(today_data[0] - past_month_data[0]) if  today_data[0] <= past_month_data[0] else ("+" + str(today_data[0] - past_month_data[0]))),
        label="The average number of times a voice contact was put on hold ",
    )

    card = models.GenericCard(
        id=1,
        title="Average customer hold time",
        value=str(today_data[0]),# Ensure this is a string
        icon="HandRaisedIcon",
        footer=cardFooter,
    )

    return card

@router.get("/card/agent/People_to_answer", tags=["card"])
async def get_People_to_answer(token: Annotated[str, Depends(requireToken)])-> models.GenericCard:
    '''
    Returns the number of people all queues
    
    ''' 
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    client = boto3.client('connect')
    
    queues_raw = await cachedData.get("list_queue")

    queues_list = []    
    
    for i in queues_raw['QueueSummaryList']:
        if i['QueueType'] == 'STANDARD':
            queues_list.append([i['Id'], i['Name']])

    response = client.get_current_metric_data(
        InstanceId=Config.INSTANCE_ID,
        Filters = {
            'Queues' : [i[0] for i in queues_list],
        },
        Groupings=['QUEUE',],
        CurrentMetrics = [
            {
                'Name': 'CONTACTS_IN_QUEUE', 
                'Unit': 'COUNT'
            }
        ],
    )

    data=0
    
    for i in response['MetricResults']:
        for n in i['Collections']:
            data += n['Value']
    
    cardFooter = models.CardFooter(
        color="text-red-500",
        value="",
        label="There are currently this many people in all queues, waiting to be answered",
    )

    card = models.GenericCard(
        id=1,
        title="People to answer",
        value=str(data), 
        icon="BriefcaseIcon",
        footer=cardFooter,
        color="green"
    )

    return card

#---------------------------------------------------------------
#----here schedule endpoints-----------------------------------
#---------------------------------------------------------------

@router.get("/card/agent/schedule", tags=["card"])
async def get_schedule(agent_id:str):

    client = boto3.client('connect')

                                   
    EndTime =  datetime.today()

    today_res = client.get_metric_data_v2(
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e' ,
        StartTime = datetime.today()-timedelta(days=31),
        EndTime = EndTime,
        Interval = {
            'TimeZone': 'UTC',
            'IntervalPeriod': 'DAY',
        },
        Filters = [
            {
            'FilterKey': 'AGENT',
            'FilterValues' : [agent_id],  
            } 
        ], 
        Metrics = [
            {
                'Name': 'AGENT_ADHERENT_TIME',
            }
        ]
    )

    data=[]

    for i in today_res['MetricResults']:
        for n in i['Collections']:
            data.append(n['Value'])
    
    return today_res
    
@router.get("/cards/capacity/agent", tags=["cards"])
async def get_capacity_agent(token: Annotated[str, Depends(requireToken)], agent_id) -> models.GenericCard:
    '''
    Returns the productive time of an agent
    '''
    if not userType.isAgent(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")
    
    client = boto3.client('connect')
    
    response = client.get_metric_data_v2(
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e' ,
        StartTime = datetime.today()-timedelta(days=1),
        EndTime = datetime.today(),
        Filters = [
            {
            'FilterKey': 'AGENT',
            'FilterValues' : [agent_id],  
            } 
        ], 
        Metrics = [
            {
                'Name': 'AGENT_OCCUPANCY',
            }
        ]
    )

    response2 = client.get_metric_data_v2(
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e' ,
        StartTime = datetime.today() - timedelta(days=30),
        EndTime = datetime.today(),
        Interval = {
            'TimeZone': 'UTC',
            'IntervalPeriod': 'TOTAL',
        },
        Filters = [
            {
            'FilterKey': 'AGENT',
            'FilterValues' : [agent_id],  
            } 
        ], 
        Metrics = [
            {
                'Name': 'AGENT_OCCUPANCY',
            }
        ]
    )

    try:
        
        datares1 = []
        for i in response['MetricResults']:
            for n in i['Collections']:
                datares1.append(n['Value'])
                print(datares1)
        
        datares2 = []
        for i in response2['MetricResults']:
            for n in i['Collections']:
                datares2.append(n['Value'])
                # print(datares2)

        comp = datares1[0]-datares2[0]

        cardFooter = models.CardFooter(
            color = "text-red-500" if comp > 0 else "text-green-500",
            value = "{p:.2f}".format(p=comp),
            label ="more than last month" if comp > 0 else "less than last month"
        )
        
        card = models.GenericCard(
            id = 1,
            title = "porcentage of time active",
            value =  "{p:.2f}".format(p=datares1[0]),
            icon = "UserIcon",
            footer = cardFooter,
            color="blue"
        )

    # If there is no data for the agent return no data
    except:
        card = models.GenericCard(
            id = 0,
            title = "Average Handle Time",
            value =  "No data",
            icon = "UserIcon",
            footer = models.CardFooter(
                color = "text-red-500",
                value = "",
                label ="No data"
            ),
            color="blue"
        )
    
    return card

# ------------------------------ Get list of users
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
    response = await cachedData.get("list_users_data")

    return response
  
@router.get("/agent-last-contact")
async def agent_last_contact(agent_id: str):
    client = boto3.client('connect')
    
    searchRes = client.search_contacts(
        InstanceId=Config.INSTANCE_ID,
        TimeRange={
            'Type': 'CONNECTED_TO_AGENT_TIMESTAMP',
            'StartTime': datetime.now() - timedelta(days=30),
            'EndTime': datetime.now()
        },
        SearchCriteria={
            'AgentIds': [agent_id]
        },
        Sort={
            'FieldName': 'CONNECTED_TO_AGENT_TIMESTAMP',
            'Order': 'DESCENDING'
        },
        MaxResults=1
    )

    if 'Contacts' in searchRes and len(searchRes['Contacts']) > 0:
        contact_id = searchRes['Contacts'][0]['Id']

        describeRes = client.describe_contact(
            InstanceId=Config.INSTANCE_ID,
            ContactId=contact_id
        )
    
    return describeRes

@router.get("/usename", tags=["data"])
async def get_usename(agent_id:str):
    response = await cachedData.get("get_usename", agent_id=agent_id)

    return response
        

# DONT DELETE THIS ROUTE
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
            UserId=id)


        FullName = f'{response["User"]["IdentityInfo"]["FirstName"]} {response["User"]["IdentityInfo"]["LastName"]}'
        Agent_email = response["User"]["Username"]

        try:
            Agent_mobile = response["User"]["IdentityInfo"]["Mobile"]
        except:
            Agent_mobile = "Unknown"

        roleids = response['User']['SecurityProfileIds']
     
        roles = []
        for roleid in roleids:
            role = client.describe_security_profile(
                InstanceId=Config.INSTANCE_ID,
                SecurityProfileId=roleid)
            roles.append(role['SecurityProfile']['SecurityProfileName'])

        return models.AgentProfileData(name=FullName, queue='Support', rating=4, email=Agent_email, mobile=Agent_mobile, roles=roles)

    except Exception as e:
        logger.error(f"Error in get_agent_profile: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.get("/card/agent/AgentRatingAvg", tags=["card"])
async def get_agent_rating(agent_id: str, token: Annotated[str, Depends(requireToken)]) -> models.GenericCard:
    if not userType.isAgent(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be logged in to access this.")

    list = await cachedData.get('getListAgentRatings', agent_id=agent_id)

    res = [0.0, 0.0]
    for rating in list:
        res[0] += rating.rating
        res[1] += 1

    # The first value is the avg of all the ratings and the second is the number of ratings
    res[0] = res[0] / res[1]

    cardFooter = models.CardFooter(
        color="text-green-500",
        value="",
        label="The average rating of the agent",
    )

    card = models.GenericCard(
        id=1,
        title="Rating",
        value=str(res[0]),
        icon="StarIcon",
        footer=cardFooter,
        color="blue"
    )

    return card



#------ Alerts endpoints

@router.get("/alerts/supervisor/NA", tags=["alerts"])
async def get_alert_supervisor_NA():
    '''
    Sends back the message of how many agent need help.
    '''
    res = await cachedData.get("get_alert_supervisor_NA")

    return res


alert_message= []

@router.post("/alerts/supervisor/message", tags=["alerts"])
async def post_alert_supervisor_message(agent_id:str):
    '''
    Sends an alert if supervisor has a message
    '''

    data = await list_users_data()

    for i in data:
        if i['Id'] == agent_id:
            agent = i['Username']
            break

    alert= models.GenericAlert(
        Text="You have a message from agent "+ agent ,
        TextRecommendation=". You should check your messages in the chat correspondant to the agent",
        color="blue",
    )

    alert_message.append(alert)

    return None


@router.get("/alerts/supervisor/available", tags=["alerts"])
async def get_alert_supervisor_available()-> models.GenericAlert:
    '''
    returns the alert type log, if there is any available
    '''
    res = await cachedData.get("get_alert_supervisor_available")

    return res


@router.get("/alerts/supervisor/nonResponse", tags=["alerts"])
async def get_alert_supervisor_nonResponse():
    '''
    sends back the alert of the agent that has not responded during the call with the client
    '''
    res = await cachedData.get("get_alert_supervisor_nonResponse")

    return res


@router.get("/alerts/get_alerts_supervisor", tags=["alerts"])
async def get_alert_supervisor():
    '''
    sends bock the alert of the supervisor
    '''
    alerts=[]

    NA= await get_alert_supervisor_NA()
    AV= await get_alert_supervisor_available()
    NR= await get_alert_supervisor_nonResponse()

    if NA:
        alerts.append(NA)
    if AV:
        alerts.append(AV)
    if NR: 
        for i in NR:
            alerts.append(i)

    if len(alert_message) > 0:
        for i in alert_message:
            alerts.append(i)
        alert_message.clear()

    return alerts

dict_agent = {}

@router.post("/alerts/agent/message", tags=["alerts"])
async def post_alert_agent_message(agent_id:int):
    '''
    Sends an alert if agent has a message
    '''
    if str(agent_id) not in dict_agent:
        dict_agent[str(agent_id)] = 0
    
    dict_agent[str(agent_id)] += 1

    return "Ok"

@router.get("/alerts/agent/NonResponse", tags=["alerts"])
async def get_alert_agent_NonResponse(agent_id:str):
    '''
    sends back the alert of the agent that has not responded during the call with the client
    '''
    client = boto3.client('connect')

    response = client.get_metric_data_v2(
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e' ,
        StartTime = datetime.today()-timedelta(days=1),
        EndTime = datetime.today(),
        Filters = [
            {
            'FilterKey': 'AGENT',
            'FilterValues' : [agent_id ],  
            } 
        ], 

        Metrics = [
            {
                'Name': 'AGENT_NON_RESPONSE_WITHOUT_CUSTOMER_ABANDONS',
            }
        ]
    )
    data = response['MetricResults'][0] ['Collections'][0] ['Value']
    if data > 0:
        alert = models.GenericAlert(
            Text="You have not responded during the call with the client.",
            TextRecommendation="You could ask for help from a supervisor or ask the client if he has any questions.",
            color="orange",
        )   
        return alert
    else:
        alert = models.GenericAlert(
            Text="You have responded during the call with the client.",
            TextRecommendation="You have done a good job.",
            color="green",
        )
        return alert
    



@router.get("/alerts/get_alerts_agent", tags=["alerts"])
async def get_alert_agent(agent_id:str):
    '''
    sends back the alert of the agent
    '''
    alerts=[]

   # NR= await get_alert_agent_NonResponse(agent_id)

    # if NR:
    #     alerts.append(NR)
    if str(agent_id) in dict_agent:
        alerts.append(models.GenericAlert(
            Text="You have "+ str(dict_agent[str(agent_id)]) + " messages from supervisor",
            TextRecommendation=". You should check your messages in the chat",
            color="blue-gray",
            )
        )
        dict_agent[str(agent_id)] = 0

    alerts.append(models.GenericAlert(
        Text="You have a message from supervisor",
        TextRecommendation=". You should check your messages in the chat correspondant to the supervisor",
        color="blue",
        )
    )



    return alerts
