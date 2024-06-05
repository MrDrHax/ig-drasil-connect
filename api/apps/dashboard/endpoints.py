from fastapi import APIRouter, Depends, HTTPException
from . import models, crud
from typing import List
from config import Config
from typing import Annotated
from AAA.requireToken import requireToken
import AAA.userType as userType
from cache.cache_object import cachedData
from datetime import datetime , timedelta, date

import random

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
        await get_connected_agents(token),
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
        await get_People_to_answer(),
        await get_capacity_agent(token, agent_id)

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


    client = boto3.client('connect')
    response = client.list_queues(
    InstanceId=Config.INSTANCE_ID,
    )

    return response

@router.get("/routing-profiles", response_model=List[dict])
async def routing_profiles():
    

    client = boto3.client('connect')

    # Get a list of all routing profiles
    response = client.list_routing_profiles(
        InstanceId=Config.INSTANCE_ID
    )

    return response['RoutingProfileSummaryList']


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

    routing_profile_list = await routing_profiles()
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

    cardFooter = models.CardFooter(
        color ="text-green-500",
        value="",
        label="The average duration of a contact in minutes this month"
    )

    card = models.GenericCard(
        id=1,
        title="Average Call Time",
        value="{p:.2f}".format(p=data/60),
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

    routing_profile_list = await routing_profiles()
    
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
async def get_connected_agents(token: Annotated[str, Depends(requireToken)]) -> models.GenericCard:
    '''
    Returns the amount of connected users.
    '''
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")
    
    client = boto3.client('connect')

    StartTime =  datetime((date.today() - timedelta(days=31)).year,
                          (date.today() - timedelta(days=31)).month, 1)
                                   
    EndTime =  datetime((date.today() - timedelta(days=31)).year, 
                                (date.today() - timedelta(days=31)).month, 
                                (datetime(date.today().year, date.today().month, 1) - timedelta(days=1)).day,
                                23, 59, 59)
    
    past_month_res = client.search_contacts(
        InstanceId=Config.INSTANCE_ID,
        TimeRange={
            'Type': 'INITIATION_TIMESTAMP',
            'StartTime': StartTime,                                  
            'EndTime': EndTime,
        },
        
        SearchCriteria={
            'Channels': [
                'VOICE',
            ],
            'InitiationMethods': [
                'INBOUND',
            ],
        },

        Sort={
            'FieldName': 'INITIATION_TIMESTAMP',
            'Order': 'ASCENDING'
        }
    )

    today_res = client.search_contacts(
        InstanceId=Config.INSTANCE_ID,
        TimeRange={
            'Type': 'INITIATION_TIMESTAMP',
            'StartTime': datetime(datetime.now().year, datetime.now().month, datetime.now().day),
            'EndTime': datetime.now(),
        },
        
        SearchCriteria={
            'Channels': [
                'VOICE',
            ],
            'InitiationMethods': [
                'INBOUND',
            ],
        },

        Sort={
            'FieldName': 'INITIATION_TIMESTAMP',
            'Order': 'ASCENDING'
        }
    )

    past_month_AVG = round(past_month_res['TotalCount']/30)
    
    footer_info = models.CardFooter(color = "text-red-500" if today_res['TotalCount'] <= past_month_AVG else "text-green-500", 
                                    value=(str(today_res['TotalCount'] - past_month_AVG) if today_res['TotalCount'] <= past_month_AVG else ("+" + str(today_res['TotalCount'] - past_month_AVG))), 
                                    label= "than last month's average")
    card= models.GenericCard(
        id=1,
        title="Connected users",
        value=str(today_res['TotalCount']),
        icon="UserIcon",
        footer=footer_info
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

    routing_profile_list = await routing_profiles()
    
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
        value = str(comp),
        label ="more than last month" if comp > 0 else "less than last month"
    )
    
    card = models.GenericCard(
        id = 1,
        title = "Average Handle Time",
        value =  str(datares1[0]),
        icon = "UserIcon",
        footer = cardFooter
    )

    
    
    return card

@router.get("/cards/abandonment-rate", tags=["cards"])
async def get_abandonment_rate(token: Annotated[str, Depends(requireToken)]) -> models.GenericCard:

    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")
    
    #routing_profile_list = await routing_profiles()
    client = boto3.client('connect')

    queues_list = await list_queues() 

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
    
    data = []
    for i in response['MetricResults']:
        for n in i['Collections']:
            data.append(str(n['Value']))  # Correctly access the value

    card_value = float(data[0])

    # print(card_value)

    if card_value > 50.0:
        cardFooter_label = "percent higher than last months average"
        cardFooter_value = str(card_value - 50.0)
    else:
        cardFooter_label = "The abandonment rate is stable"
        cardFooter_value = "0.0"

    cardFooter = models.CardFooter(
        color="text-red-500",
        value=cardFooter_value,
        label=cardFooter_label,
    )

    card = models.GenericCard(
        id=1,
        title="Abandoment rate",
        value=data[0],  # Ensure this is a string
        icon="PhoneXMarkIcon",
        footer=cardFooter,
    )

    return card


@router.get("/graph/get-queues")
async def get_queues(token: Annotated[str, Depends(requireToken)]) -> models.GenericGraph:
    
    '''
    Returns the number of people in each queue
    
    ''' 
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    client = boto3.client('connect')   

    queues_raw = await list_queues() 

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
        footer="" ,
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
    
    queues_list = await list_queues() 

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
        title="Average Holds",
        value=str(today_data[0]),# Ensure this is a string
        icon="HandRaisedIcon",
        footer=cardFooter,
    )

    return card

@router.get("/card/agent/People_to_answer", tags=["card"])
async def get_People_to_answer()-> models.GenericCard:
    '''
    Returns the number of people all queues
    
    ''' 
    # if not userType.isManager(token):
    #     raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    client = boto3.client('connect')
    
    queues_raw = await list_queues() 

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
                print(datares2)

        comp = datares1[0]-datares2[0]

        cardFooter = models.CardFooter(
            color = "text-red-500" if comp > 0 else "text-green-500",
            value = str(comp),
            label ="more than last month" if comp > 0 else "less than last month"
        )
        
        card = models.GenericCard(
            id = 1,
            title = "Average Handle Time",
            value =  str(datares1[0]),
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
    
    

    client = boto3.client('connect')

    # Get info about the users of said instance
    response = client.list_users(
        InstanceId=Config.INSTANCE_ID,
    )

    return response['UserSummaryList']

# # ---------------------------------------------------- Volver a checar (requiere numero de telefono)
# @router.get("/get-current-metric-data")
# async def check_agent_availability(queue_id: str):
#     """
#     Description:
#         Real-time information of the call.
#     Parameters:
#         * InstanceId [REQUIRED][string]: id of the Amazon Connect instance.
#         * Filters [REQUIRED][dictionary]:  
#             - 

#     Read the docs:
#     https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_current_metric_data.html#

#     @return 
#         Metrics about an on-going call.

#         ex. queue_id = '18494127-588c-4497-8291-9dacaee44341'
#     """    


#     client = boto3.client('connect')

#     # Get info for the first routing profile
#     response = client.get_current_metric_data(
#         InstanceId=Config.INSTANCE_ID,
#         Filters={
#             'Queues': [queue_id],

#             'Channels': [
#                 'VOICE'
#             ]
#         },
#         CurrentMetrics=[
#         {
#             'Name': 'AGENTS_ONLINE',
#             'Unit': 'COUNT'
#         },
#         ]
#     )

#     return response['MetricResults']

#     # data = cachedData.get("check_agent_availability_data")

#     # return data
# # -------------------------------------------------Needs review
# # @router.get("/agent-status", response_model=List[dict])
# # async def check_agent_availability():
# #     """
# #     Description:
# #         Verifies the status of agents in Amazon Connect.
# #         It can be one of four things:

# #         * AVAILABLE: on-duty and not in call
# #         * OFFLINE: not on-duty and disconnected
# #         * BUSY: with an open thread or ongoing call
# #         * NEEDS ASSISTANCE: needs help from supervisor

# #     Parameters:
# #         * InstanceId [REQUIRED][string]: amazon connect instance identified
# #         * AgentStatusTypes [list]: The available agent status types
# #         * PaginationConfig [dictionary]
# #             * MaxItems [int]: total number of items to return
# #             * PageSize [int]: the size of each page
        
# #     Read the docs:
# #     https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListAgentStatuses.html

# #     @return 
# #         List containing the availability status of agents. (Not yet known)
# #     """

# #     client = boto3.client('connect')
# #     paginator = client.get_paginator('list_agent_statuses')

# #     # Get info for the first routing profile
# #     response_iterator = paginator.paginate(
# #         InstanceId = Config.INSTANCE_ID,
# #         AgentStatusTypes = [
# #             'AVAILABLE','OFFLINE','BUSY','ON BREAK','NEEDS ASSISTANCE',
# #         ])
    
# #     return response_iterator


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

# # list_recommenders_cache = []

# # @router.get("/list-recommenders", response_model=List[dict])
# # async def list_recommenders():
# #     try:
# #         client = boto3.client('connect')
# #         response = client.list_queues(
# #             InstanceId='string',
# #             MaxResults=10
# #         )
        
# #         return response
# #     except Exception as e: 
# #         print(e.with_traceback)
# #         print(e)
        

# @router.get("/call-summary")
# async def call_summary():
#     """
#     Description:
#         Returns a series of metrics of a call with a certain contact specified by id

#     Parameters:
#         * InstanceId [REQUIRED][string]: amazon connect instance identified
#         * ContactId [REQUIRED][string]: identifier of the contact
        
#     Read the docs:
#     https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/describe_contact.html

#     @return 
#         JSON with the information on the call
#     """
#     try:
#         client = boto3.client('connect')
#         response = client.describe_contact(
#             InstanceId=Config.INSTANCE_ID,
#             ContactId='string'
#         )
        
#         return response
#     except Exception as e: 
#         print(e.with_traceback)
#         print(e)

# @router.get("/agent-status", response_model=List[dict])
# async def agent_status():
    
#     '''
#     Returns the agent status.
    
#     '''
    
#     client = boto3.client('connect')
#     response = client.list_agent_statuses(
#         InstanceId=Config.INSTANCE_ID
#     )
    
#     return response['AgentStatusSummaryList']    

# @router.get("/queue-description")
# async def queue_description(queue_id: str):
#     client = boto3.client('connect')
#     response = client.describe_queue(
#         InstanceId=Config.INSTANCE_ID,
#         QueueId=queue_id
#     )
    
#     return response['Queue']

# @router.get("/describe-routing-profile")
# async def describe_routing_profile(routing_profile_id: str):
#     client = boto3.client('connect')
#     response = client.describe_routing_profile(
#         InstanceId=Config.INSTANCE_ID,
#         RoutingProfileId=routing_profile_id
#     )
    
#     return response['RoutingProfile']


# @router.get("/list-routing-profile-queues")
# async def list_routing_profile_queues(routing_profile_id: str):
#     client = boto3.client('connect')

#     response = client.list_routing_profile_queues(
#         InstanceId=Config.INSTANCE_ID,
#         RoutingProfileId=routing_profile_id
#     )['RoutingProfileQueueConfigSummaryList']
    
#     return response

# @router.get("/describe-contact")
# async def describe_contact(contact_id: str):

#     client = boto3.client('connect')
#     response = client.describe_contact(
#         InstanceId=Config.INSTANCE_ID,
#         ContactId=contact_id
#     )

#     return response['Contact']

# # 802dc0a071714366b20b7dd891929556
# @router.get("/desciribe-user")
# async def describe_user(user_id:str):

#     client = boto3.client('connect')
#     response = client.describe_user(
#         InstanceId=Config.INSTANCE_ID,
#         UserId= user_id
#     )
#     return response['User']


# # @router.get("/get-transcript")
# # async def get_transcript(Contacd_Id: str, Connection_Token: str):

# #     client = boto3.client('connectparticipant')
# #     response = client.get_transcript(
# #         ContactId = Contacd_Id,
# #         ConnectionToken = request.cookies['access_token'], # Requerimos este token de autenticación.
# #     )
# #     return response['User']


# @router.get("/metric-data")
# async def metric_data(queue_id:str):

#     client = boto3.client('connect')
#     response = client.get_metric_data(
#         InstanceId=Config.INSTANCE_ID,
#         StartTime=datetime(2024, 5, 25, 0),
#         EndTime=datetime(2024, 5, 25, 16),
#         Filters={
#             'Queues': [
#                 queue_id
#                 ]
#         },
#         Groupings=[
#             'QUEUE'
#         ],
#         HistoricalMetrics=[
#             {
#                 'Name': 'INTERACTION_TIME',
#             # 'Threshold': {
#             #     'Comparison': 'LT',
#             #     'ThresholdValue': 123.0
#             # },
#                 'Statistic': 'AVG',
#                 'Unit': 'SECONDS'
#             },
#         ]
#     )

#     print(response)

#     return response['MetricResults']

# @router.get("/current-metric-data")
# async def current_metric_data(queue_id:str):

#     client = boto3.client('connect')
#     response = client.get_current_metric_data(
#         InstanceId=Config.INSTANCE_ID,
#         Filters={
#             'Queues': [
#                 queue_id
#             ],
#             'Channels': [
#                 'VOICE'
#             ]
#         },
#         Groupings=['QUEUE'],
#         CurrentMetrics=[
#         {
#             'Name': 'AGENTS_AVAILABLE',
#             'Unit': 'COUNT'
#         },
#         ]
#     )

#     print(response)

#     return response['MetricResults']


# @router.get("/current-user-data")
# async def get_current_user_data():

#     client = boto3.client('connect')
#     response = client.get_current_user_data(
#         InstanceId=Config.INSTANCE_ID,
#         Filters={
#             'Agents': [
#                 '1c38eb16-8f2c-4c9a-b723-8f0621583179',
#                 '270a9b75-7c3d-40de-b524-25011c6aeeb8',
#                 '305376be-597e-4c30-8cc1-d0ceb88699fe',
#                 '35eb516c-0c56-45a2-ab53-b09a43f196c3',
#                 '50f98823-5278-47fb-8c1a-e56fa525404a',
#                 '51ec1227-4119-412e-b0e6-2e3bbc6ae1a4',
#                 '7688a303-17b8-4402-b03f-d7ab051bde4e',
#                 '7d6be46a-287b-48fc-8bdb-70655a978247',
#                 '83656f24-be8f-4cc6-aca9-c3bf5c42e21a',
#                 '8d6f58c4-d1f5-4024-9ab0-c57666dd791b',
#                 '94c89e21-3aac-44b5-8ffa-c898061fddfd',
#                 'a3f8c7e6-712c-4c13-a9ae-5ed13e1f6523',                
#                 'b2ba1a5d-6f46-40a5-aa24-6b5032bf79fd',
#                 'ba862485-c72a-4fb9-8f98-58415b19482b',
#                 'c6437a67-db38-49da-8188-778ac2f1f555',
#                 'cf1410c7-01e9-484a-971a-e481924ee68e',
#                 'd2eed6e2-7bef-4983-83c8-cfd359d8cdbd',
#                 'fb1b7cb4-2e81-4d16-a50e-9726de5cc15a'
#             ],
#         #    'ContactFilter': {
#         #         'ContactStates': [
#         #             'CONNECTED'
#         #         ]
#         #     },
#         },
#         # CurrentMetrics=[
#         # {
#         #     'Name': 'AGENTS_AVAILABLE',
#         #     'Unit': 'COUNT'
#         # },
#         # ]
#     )

#     print(response)

#     return response['UserDataList']


# @router.get("/list-contacts")
# async def list_contacts():

#     client = boto3.client('connect')
#     response = client.search_contacts(
#         InstanceId=Config.INSTANCE_ID,
#         TimeRange={
#             'Type': 'INITIATION_TIMESTAMP',
#             # |'SCHEDULED_TIMESTAMP'|'CONNECTED_TO_AGENT_TIMESTAMP'|'DISCONNECT_TIMESTAMP',
#             'StartTime': datetime.today() - timedelta(days=56),
#             'EndTime': datetime.today(),
#         },
        
#         SearchCriteria={
#             'Channels': [
#                 'VOICE',
#             ],
#             'InitiationMethods': [
#                 'INBOUND',
#                 # |'OUTBOUND'|'TRANSFER'|'QUEUE_TRANSFER'|'CALLBACK'|'API'|'DISCONNECT'|'MONITOR'|'EXTERNAL_OUTBOUND',
#             ],
#         },

#         Sort={
#             'FieldName': 'INITIATION_TIMESTAMP',
#             # |'SCHEDULED_TIMESTAMP'|'CONNECTED_TO_AGENT_TIMESTAMP'|'DISCONNECT_TIMESTAMP'|'INITIATION_METHOD'|'CHANNEL',
#             'Order': 'ASCENDING'
#             # |'DESCENDING'
#         }
#     )

#     print(response)

#     return response['Contacts']