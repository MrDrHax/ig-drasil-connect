from fastapi import APIRouter, Depends, HTTPException
from . import models, crud
from typing import List
from config import Config
from typing import Annotated
from AAA.requireToken import requireToken
import AAA.userType as userType
from cache.cache_object import cachedData
from datetime import datetime , timedelta, date,timezone
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
        await read_capacity(token),
        await read_average_call_time(token),
        await read_connected_users(token),
        # await get_avg_handle_time(),
        await read_abandonment_rate(token),
        # await get_avg_holds(token),
    ]

    graphs = [
        await graph_example(),
        await read_avg_contact_duration(token),
        await read_queues(token),  
    ]

    toReturn = models.DashboardData(cards=cards, graphs=graphs)

    return toReturn

@router.get("/agent_cards", tags=["agent_view"])
async def get_agent_cards(token: Annotated[str, Depends(requireToken)], agent_id: str) -> models.DashboardData:
    '''
    Returns the cards that will be displayed on the agent dashboard.
    '''
    cards = [
        await read_avg_holds(token, agent_id),
        await read_People_to_answer(token),
        await read_capacity_agent(token, agent_id),
        await get_agent_rating(agent_id, token)
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
async def read_list_queues():

    response =await cachedData.get("list_queue")

    return response

@router.get("/routing-profiles", response_model=List[dict])
async def read_routing_profiles():
    
    response = await cachedData.get("list_routing_profile")

    return response

@router.get("/get-online-users-data")
async def read_online_users_data(token: Annotated[str, Depends(requireToken)]):
    
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    response = await cachedData.get("online_users_data")
    
    return response

@router.get("/not-connected-users-data")
async def read_not_connected_users_data(token: Annotated[str, Depends(requireToken)]):
    
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    response = await cachedData.get("get_not_connected_users_data")
    
    return response


@router.get("/average-call-time-duration")
async def read_average_call_time(token: Annotated[str, Depends(requireToken)])->models.GenericCard:
    
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    response = await cachedData.get("get_avg_call_time")
    
    return response

@router.get("/graph/get-avg-contact-duration")
async def read_avg_contact_duration(token: Annotated[str, Depends(requireToken)])-> models.GenericGraph:
    
    '''
    Returns the average contact duration.
    
    ''' 
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    response = await cachedData.get("get_avg_contact_duration")
    
    return response


@router.get("/connected/users" , tags=["cards"])
async def read_connected_users(token: Annotated[str, Depends(requireToken)]) -> models.GenericCard:
    '''
    Returns the amount of connected agents.
    '''
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    response = await cachedData.get("get_connected_users")
    
    return response

@router.get("/cards/capacity", tags=["cards"])
async def read_capacity(token: Annotated[str, Depends(requireToken)]) -> models.GenericCard:
    '''
    Returns the capacity
    '''
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")
    
    response = await cachedData.get("get_capacity")
    
    return response

@router.get("/cards/abandonment-rate", tags=["cards"])
async def read_abandonment_rate(token: Annotated[str, Depends(requireToken)]) -> models.GenericCard:

    # TODO fix this hot trash

    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")
    
    response = await cachedData.get("get_abandonment_rate")
    
    return response

@router.get("/graph/get-queues")
async def read_queues(token: Annotated[str, Depends(requireToken)]) -> models.GenericGraph:
    
    '''
    Returns the number of people in each queue
    
    ''' 
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")
    
    response = await cachedData.get("get_queues")
    
    return response


# aqui va parte del agente hasta que funcione el dashboard agent


@router.get("/agent/avg-holds", tags=["agent"])
async def read_avg_holds(token: Annotated[str, Depends(requireToken)],agent_id:str)-> models.GenericCard:
    '''
    The average hold time of an agent in the last 30 days 
    '''

    if not userType.isAgent(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    response = await cachedData.get("get_avg_holds", agent_id=agent_id)
    
    return response

@router.get("/card/agent/People_to_answer", tags=["card"])
async def read_People_to_answer(token: Annotated[str, Depends(requireToken)])-> models.GenericCard:
    '''
    Returns the number of people all queues
    
    ''' 
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    response = await cachedData.get("get_People_to_answer")
    
    return response

#---------------------------------------------------------------
#----here schedule endpoints-----------------------------------
#---------------------------------------------------------------

@router.get("/card/agent/schedule", tags=["card"])
async def read_schedule(agent_id:str, token: Annotated[str, Depends(requireToken)])-> models.GenericCard:

    if not userType.isAgent(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    response = await cachedData.get("get_schedule", agent_id=agent_id)
        
    return response

@router.get("/cards/capacity/agent", tags=["cards"])
async def read_capacity_agent(token: Annotated[str, Depends(requireToken)], agent_id) -> models.GenericCard:
    '''
    Returns the productive time of an agent
    '''
    if not userType.isAgent(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")
    
    response = await cachedData.get("get_capacity_agent", agent_id=agent_id)
    
    return response

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
        icon="Star",
        footer=cardFooter,
        color="blue"
    )

    return card

#------ Alerts endpoints

@router.get("/alerts/supervisor/NA", tags=["alerts"])
async def get_alert_supervisor_NA(token: Annotated[str, Depends(requireToken)]):
    '''
    Sends back the message of how many agent need help.
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
    if not userType.isManager(token):
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
    if not userType.isAgent(token) or not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    res = await cachedData.get("get_alert_supervisor_available")

    return res


@router.get("/alerts/supervisor/nonResponse", tags=["alerts"])
async def get_alert_supervisor_nonResponse(token: Annotated[str, Depends(requireToken)]):
    '''
    sends back the alert of the agent that has not responded during the call with the client
    '''
    if not userType.isAgent(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")
    res = await cachedData.get("get_alert_supervisor_nonResponse")

    return res


@router.get("/alerts/get_alerts_supervisor", tags=["alerts"])
async def get_alert_supervisor(token: Annotated[str, Depends(requireToken)]):
    '''
    sends bock the alert of the supervisor
    '''
    if not userType.isAgent(token) or not userType.isManager(token):
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
    if not userType.isAgent(token) or not userType.isManager(token):
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
    if not userType.isAgent(token) or not userType.isManager(token):
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
    if not userType.isAgent(token) or not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

    client = boto3.client('connect')
    agent= await list_users_data()

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
                    Text="You have a non response a call with the client",
                    TextRecommendation=". You asked to respond to the client during the call or asker for help to the supervisor",
                    color="red",
                    timestamp= datetime.now(tz=timezone.utc).strftime('%Y-%m-%d %H:%M')
                )
            else:
                return models.GenericAlert(
                    Text="You have a non response a call with the client",
                    TextRecommendation=". you good job, you have responded to the client during the call",
                    color="green",
                    timestamp= datetime.now(tz=timezone.utc).strftime('%Y-%m-%d %H:%M')
                )
    return models.GenericAlert(
        Text="You have a non response a call with the client",
        TextRecommendation=". you good job, you have responded to the client during the call",
        color="green",
        timestamp= datetime.now(tz=timezone.utc).strftime('%Y-%m-%d %H:%M')
    )

    

@router.get("/alerts/get_alerts_agent", tags=["alerts"])
async def get_alert_agent(agent_id:str, token: Annotated[str, Depends(requireToken)]):
    '''
    sends back the alert of the agent
    '''
    if not userType.isAgent(token) or not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")

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
