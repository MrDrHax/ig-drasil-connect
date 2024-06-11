from fastapi import APIRouter, Depends, HTTPException
from . import models, crud
from typing import List
from typing import Annotated
from config import Config
from datetime import datetime , timedelta, date
from cache.cache_object import cachedData


import boto3

router = APIRouter(
    prefix="/dashboardAgents",
    tags=["dashboardAgents"],
    responses={
        200: {"description": "Success"},
        # 202: {"description": "Accepted, request is being processed. Applies for connect requests that might take a while."},
        400: {"description": "Bad request, parameters are missing or invalid"},
        401: {"description": "Unauthorized. The request was not authorized."},
        404: {"description": "Not found"},
        500: {"description": "Internal server error, unknown error occurred."},
        503: {"description": "Service unavailable. Amazon Connect did not respond."},
    }
)


# @router.get("/routing-profiles", response_model=List[dict])
# async def routing_profiles():
    

#     client = boto3.client('connect')

#     # Get a list of all routing profiles
#     response = client.list_routing_profiles(
#         InstanceId=Config.INSTANCE_ID
#     )

#     return response['RoutingProfileSummaryList']



# @router.get("/data/connected", tags=["data"])
# async def get_current_user_data() -> int:
#     '''
#     Returns the time the agent is connected to a call.

#     '''

#     return 20

# async def get_agent_rating(agent_id: str) -> float:
#     '''
#     Returns the rating of a given agent, based on their Id.

#     agent_id: The identifier of the agent account

#     Returns: The rating of the agent
#     '''

#     # Crea un cliente de boto3 para interactuar con Amazon Connect
#     client = boto3.client('connect')

#     # Llama a la función describe_user para obtener información del agente
#     response = client.describe_user(
#         InstanceId=Config.INSTANCE_ID,
#         UserId=agent_id
#     )

#     # En este ejemplo, supongamos que el rating del agente está en el campo 'Rating'
#     agent_rating = response['User']['Rating']

#     return agent_rating


# @router.get("/agent_rating/{agent_id}", tags=["ratings"])
# async def get_agent_rating_by_id(agent_id: str):
#     '''
#     Retrieves the rating of an agent based on the provided agent ID.
#     '''
#     # Llama a la función get_agent_rating para obtener el rating del agente
#     agent_rating = await get_agent_rating(agent_id)

#     return agent_rating


# @router.get("/agent/current-cases", tags=["agent"])
# async def get_current_cases():
#     '''
#     The total count of cases existing in a given domain. 
#     '''
    
#     routing_profile_list = await routing_profiles()
#     client = boto3.client('connect')
    
#     response = client.get_metric_data_v2(
#         ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e' ,
#         StartTime = datetime.today() - timedelta(days=30),
#         EndTime = datetime.today(),
#         Interval = {
#             'TimeZone': 'UTC',
#             'IntervalPeriod': 'TOTAL',
#         },
#         Filters = [
#             {
#             'FilterKey': 'ROUTING_PROFILE',
#             'FilterValues' : [i['Id'] for i in routing_profile_list],  
#             } 
#         ], 
#         Metrics = [
#             {
#                 'Name': 'CURRENT_CASES',
#             }
#         ]
#     )

#     data = []
#     for i in response['MetricResults']:
#         for n in i['Collections']:
#             data.append(str(n['Value']))
    
#     cardFooter = models.CardFooter(
#         color="text-red-500",
#         value="",
#         label="The total count of cases existing this month",
#     )

#     card = models.GenericCard(
#         id=1,
#         title="Current Cases",
#         value=data[0],  # Ensure this is a string
#         icon="BriefcaseIcon",
#         footer=cardFooter,
#     )

#     return card

# @router.get("/card/agent/People_to_answer", tags=["card"])
# async def get_People_to_answer():
#     '''
#     Returns the number of people all queues
    
#     ''' 
    
#     client = boto3.client('connect')
    
#     queues_raw = await list_queues() 

#     queues_list = []    
    
#     for i in queues_raw['QueueSummaryList']:
#         if i['QueueType'] == 'STANDARD':
#             queues_list.append([i['Id'], i['Name']])

#     response = client.get_current_metric_data(
#         InstanceId=Config.INSTANCE_ID,
#         Filters = {
#             'Queues' : [i[0] for i in queues_list],
#         },
#         Groupings=['QUEUE',],
#         CurrentMetrics = [
#             {
#                 'Name': 'CONTACTS_IN_QUEUE', 
#                 'Unit': 'COUNT'
#             }
#         ],
#     )

#     data=0
    
#     for i in response['MetricResults']:
#         for n in i['Collections']:
#             data += n['Value']
    
#     cardFooter = models.CardFooter(
#         color="text-red-500",
#         value="",
#         label="There are currently this many people in all queues, waiting to be answered",
#     )

#     card = models.GenericCard(
#         id=1,
#         title="People to answer",
#         value=str(data), 
#         icon="BriefcaseIcon",
#         footer=cardFooter,
#     )

#     return card