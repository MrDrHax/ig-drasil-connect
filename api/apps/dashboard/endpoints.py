from fastapi import APIRouter, Depends, HTTPException
from . import models, crud
from typing import List
from config import Config
from typing import Annotated
from AAA.requireToken import requireToken
import AAA.userType as userType
from cache.cache_object import cachedData
from datetime import datetime , timedelta, date, timezone
from tools.lazySquirrel import LazySquirrel

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
        await get_connected_users(token),
        # await get_avg_handle_time(),
        await get_abandonment_rate(token),
        # await get_avg_holds(token),
    ]

    graphs = [
        await get_avg_contact_duration(token),
        await get_queues(token),  
    ]

    toReturn = models.DashboardData(cards=cards, graphs=graphs)

    return toReturn

@router.get("/agent_cards", tags=["agent_view", "cards"])
async def get_agent_cards(token: Annotated[str, Depends(requireToken)], agent_id: str) -> models.DashboardData:
    '''
    Returns the cards that will be displayed on the agent dashboard.
    '''
    cards = [
        await get_avg_holds(token, agent_id),
        await get_People_to_answer(token),
        await get_capacity_agent(token, agent_id),
        await get_agent_rating(agent_id, token)
    ]

    graphs = [
    ]

    toReturn = models.DashboardData(cards=cards, graphs=graphs)

    return toReturn

# @router.get("/routing-profiles", response_model=List[dict])
# async def routing_profiles():
    
#     response = await cachedData.get("list_routing_profile")

#     return response

# @router.get("/get-online-users-data")
# async def get_online_users_data():

#     client = boto3.client('connect')
#     users = client.list_users(
#         InstanceId=Config.INSTANCE_ID,
#     )
#     userList = []
#     for user in users['UserSummaryList']:
#         userList.append(user['Id'])

#     response = client.get_current_user_data(
#         InstanceId=Config.INSTANCE_ID,
#         Filters={
#             'Agents': userList
#         }
#     )
#     return response['UserDataList']

# @router.get("/get-not-connected-users-data")
# async def get_not_connected_users_data():

#     client = boto3.client('connect')
#     users = client.list_users(
#         InstanceId=Config.INSTANCE_ID,
#     )
#     userList = []
#     for user in users['UserSummaryList']:
#         userList.append(user['Id'])

#     response = client.get_current_user_data(
#         InstanceId=Config.INSTANCE_ID,
#         Filters={
#             'Agents': userList
#         }
#     )

#     for user in response['UserDataList']:
#         if user['User']['Id'] in userList:
#             userList.remove(user['User']['Id'])

#     return userList

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
        value = "{p:.2f}".format(p=extra) + " min",
        label = ("less than recommended" if extra < 3 else "more than recommended") + ". The average duration of a contact in minutes this month. Calls should be less than 3 minutes."
    )

    card = models.GenericCard(
        id=1,
        title="Average Call Time",
        value="{p:.2f}".format(p=data/60) + "min",
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
    
    datares2 = []
    for i in response2['MetricResults']:
        for n in i['Collections']:
            datares2.append(n['Value'])


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
    '''get the abandonment rate of the calls. used for dashboard cards'''

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

    if (card_value > 80):
        footerColor = "text-red-500"
        footerSpecialText = f'{(card_value - 80):.2f}%'
        footerDesc = 'more than the recommended rate.'
    elif (card_value > 50):
        footerColor = "text-orange-500"
        footerSpecialText = f'{(card_value - 50):.2f}%'
        footerDesc = 'more than the recommended rate.'
    else:
        footerColor = "text-green-500"
        footerSpecialText = f'{(50 - card_value):.2f}%'
        footerDesc = 'less than the recommended rate.'

    cardFooter = models.CardFooter(
        color=footerColor,
        value=footerSpecialText,
        label=footerDesc + " The abandonment rate is the amount of calls that where ended by the user before having contact with an agent. The recommended rate is 50%.",
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

    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")
    
    queue_data = await cachedData.get("get_queues_data")

    return models.GenericGraph(
        id = 1,
        title = "Clients by Queue",
        description = "The number of people in each queue",
        footer = "Updated " + datetime.today().strftime('%Y-%m-%d') ,
        chart = models.ChartData(
            type = "bar",
            series = [
                models.SeriesData(name = "Max Queue Size",data = [q['maxContacts'] for q in queue_data]),
                models.SeriesData(name = "Current Queue Size",data = [q['waiting'] for q in queue_data])
            ],
            options = models.GraphOptions(
                xaxis = models.XAxisData(categories = [q['name'] for q in queue_data]))
        )
    )

# Agent Dashboard

@router.get("/agent/avg-holds", tags=["agent"])
async def get_avg_holds(token: Annotated[str, Depends(requireToken)], agent_id:str)-> models.GenericCard:
    '''
    The total count of cases existing in a given domain. 
    '''

    if not userType.isAgent(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    ret = await cachedData.get("get_avg_holds", agent_id=agent_id)

    return ret

@router.get("/card/agent/People_to_answer", tags=["card"])
async def get_People_to_answer(token: Annotated[str, Depends(requireToken)])-> models.GenericCard:
    '''
    Returns the number of people all queues
    
    ''' 
    if not userType.isAgent(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")
    
    ret = await cachedData.get("get_People_to_answer")

    return ret

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
        value= "{p:.2f}".format(p=res[0]),
        icon="Star",
        footer=cardFooter,
        color="blue"
    )

    return card

@router.get("/cards/capacity/agent", tags=["cards"])
async def get_capacity_agent(token: Annotated[str, Depends(requireToken)], agent_id) -> models.GenericCard:
    '''
    Returns the productive time of an agent
    '''
    if not userType.isAgent(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")
    
    ret = await cachedData.get("get_capacity_agent", agent_id=agent_id)

    return ret

# ------------------------------ Get list of users
@router.get("/list-users-data", response_model=List[dict])
async def list_users_data(token: Annotated[str, Depends(requireToken)]):
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
    if not userType.isManager(token) and not userType.isAgent(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    response = await cachedData.get("list_users_data")

    return response
        
#------ Agent Profile
@router.get("/agent-profile", tags=["profile"])
async def get_agent_profile(id: str, token: Annotated[str, Depends(requireToken)]) -> models.AgentProfileData:
    '''
    Returns the profile of an agent.

    To get the full list, go to /lists/agents
    '''
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")
    
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

#------ Alerts endpoints

@router.get("/alerts/supervisor/NA", tags=["alerts"])
async def get_alert_supervisor_NA(token: Annotated[str, Depends(requireToken)]):
    '''
    Sends back the message of how many agents need help.
    '''
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    res = await cachedData.get("get_alert_supervisor_NA")

    return res

alert_message= []

@router.post("/alerts/supervisor/message", tags=["alerts"])
async def post_alert_supervisor_message(agent_id:str, token: Annotated[str, Depends(requireToken)]):
    '''
    Sends an alert if supervisor has a message
    '''
    if not userType.isManager(token) and not userType.isAgent(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    data = await list_users_data()

    for i in data:
        if i['Id'] == agent_id:
            agent = i['Username']
            break

    alert= models.GenericAlert(
        Text="You have a message from agent "+ agent ,
        TextRecommendation=". You should check your messages in the chat correspondant to the agent",
        color="blue",
        timestamp= datetime.now(tz=timezone.utc).strftime('%Y-%m-%d %H:%M')
    )

    alert_message.append(alert)

    return None


@router.get("/alerts/supervisor/available", tags=["alerts"])
async def get_alert_supervisor_available( token: Annotated[str, Depends(requireToken)])-> models.GenericAlert:
    '''
    returns the alert type log, if there is any available
    '''
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    res = await cachedData.get("get_alert_supervisor_available")

    return res

@router.get("/alerts/supervisor/nonResponse", tags=["alerts"])
async def get_alert_supervisor_nonResponse(token: Annotated[str, Depends(requireToken)]):
    '''
    sends back the alert of the agent that has not responded during the call with the client
    '''
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")
    res = await cachedData.get("get_alert_supervisor_nonResponse")

    return res

@router.get("/alerts/get_alerts_supervisor", tags=["alerts"])
async def get_alert_supervisor(token: Annotated[str, Depends(requireToken)]):
    '''
    sends bock the alert of the supervisor
    '''
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    alerts=[]

    NA= await get_alert_supervisor_NA(token)
    AV= await get_alert_supervisor_available(token)
    NR= await get_alert_supervisor_nonResponse(token)

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

alert_message_agent= []

@router.post("/alerts/agent/message", tags=["alerts"])
async def post_alert_agent_message(token: Annotated[str, Depends(requireToken)]):
    '''
    Sends an alert if agent has a message
    '''
    if not userType.isAgent(token) and not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    alert= models.GenericAlert(
        Text="You have a message from supervisor",
        TextRecommendation=". You should check your messages in the chat correspondant to the supervisor",
        color="blue-gray",
        timestamp= datetime.now(tz=timezone.utc).strftime('%Y-%m-%d %H:%M')
    )

    alert_message_agent.append(alert)

    return "Ok"

dict_agent = {}

@router.post("/alerts/agent/message", tags=["alerts"])
async def post_alert_agent_message(agent_id:int, token: Annotated[str, Depends(requireToken)]):
    '''
    Sends an alert if agent has a message
    '''
    if not userType.isAgent(token) and not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    if str(agent_id) not in dict_agent:
        dict_agent[str(agent_id)] = 0
    
    dict_agent[str(agent_id)] += 1

    return "Ok"

@router.get("/alerts/agent/NonResponse", tags=["alerts"])
async def get_alert_agent_NonResponse(agent_id:str, token: Annotated[str, Depends(requireToken)]):
    '''
    sends back the alert of the agent that has not responded during the call with the client
    '''
    if not userType.isAgent(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be an agent to access this resource.")

    client = boto3.client('connect')
    agent = await list_users_data(token)

    response = client.get_metric_data_v2(
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e' ,
        StartTime = datetime.today()-timedelta(days=1),
        EndTime = datetime.today(),
        Filters = [
            {
            'FilterKey': 'AGENT',
            'FilterValues' : [i['Id'] for i in agent],  
            } 
        ], 

        Groupings=['AGENT', ],

        Metrics = [
            {
                'Name': 'AGENT_NON_RESPONSE_WITHOUT_CUSTOMER_ABANDONS',
            }
        ]
    )

    for i in response['MetricResults']:
        if i["Dimensions"]["AGENT"] == agent_id:
            if i['Collections'][0]['Value'] > 0:
                return models.GenericAlert(
                    Text="You did not respond to a call with the client",
                    TextRecommendation=". You should pay more attention to incoming calls in the future",
                    color="red",
                    timestamp= datetime.now(tz=timezone.utc).strftime('%Y-%m-%d %H:%M')
                )
            else:
                return models.GenericAlert(
                    Text="You responded to a call with a client",
                    TextRecommendation=". You did a good job, you should continue with your work",
                    color="green",
                    timestamp= datetime.now(tz=timezone.utc).strftime('%Y-%m-%d %H:%M')
                )
    return models.GenericAlert(
        Text="You responded to all calls with clients",
        TextRecommendation=". You did a good job, you should continue with your work",
        color="green",
        timestamp= datetime.now(tz=timezone.utc).strftime('%Y-%m-%d %H:%M')
    )

@router.get("/alerts/get_alerts_agent", tags=["alerts"])
async def get_alert_agent(agent_id:str, token: Annotated[str, Depends(requireToken)]):
    '''
    sends back the alert of the agent
    '''
    if not userType.isAgent(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be an agent to access this resource.")

    alerts=[]

    NR= await get_alert_agent_NonResponse(agent_id, token)

    if NR:
        alerts.append(NR)
    if str(agent_id) in dict_agent and dict_agent[str(agent_id)] > 0:
        alerts.append(models.GenericAlert(
            Text="You have "+ str(dict_agent[str(agent_id)]) + " messages from supervisor",
            TextRecommendation=". You should check your messages in the chat",
            color="blue-gray",
            timestamp= datetime.now(tz=timezone.utc).strftime('%Y-%m-%d %H:%M')
            )
        )
        dict_agent[str(agent_id)] = 0


    return alerts
