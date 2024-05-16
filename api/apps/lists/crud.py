from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from config import Config
from cache.cache_object import cachedData

import logging
logger = logging.getLogger(__name__)

async def get_routing_profile_list():
    client = boto3.client('connect')

    # Get a list of all routing profiles
    response = client.list_routing_profiles(
        InstanceId=Config.INSTANCE_ID
    )

    return response['RoutingProfileSummaryList']

cachedData.add("get_routing_profile_list", get_routing_profile_list, 30) # 24 hours

async def get_routingProfilesArns():
    routingProfiles = await cachedData.get('get_routing_profile_list')
    return [profile['Arn'] for profile in routingProfiles]

cachedData.add("get_routingProfilesArns", get_routingProfilesArns, 30) # 24 hours

async def get_agent_name_data(id: str) -> str:
    client = boto3.client('connect')
    response = client.describe_user(
        InstanceId=Config.INSTANCE_ID,
        UserId=id
    )
    return f"{response['User']['IdentityInfo']['FirstName']} {response['User']['IdentityInfo']['LastName']}"

cachedData.add("get_agent_name_data", get_agent_name_data, 60*24) # 24 hours

async def get_routing_profile_name_data(id: str):
    routing_profile_list = await cachedData.get('get_routing_profile_list')

    for profile in routing_profile_list:
        if profile['Id'] == id:
            return profile['Name']

cachedData.add("get_routing_profile_name_data", get_routing_profile_name_data, 60*24) # 24 hours

async def routing_profiles_data() -> tuple:
    client = boto3.client('connect')

    # Get a list of all routing profiles
    # response = client.list_routing_profiles(
    #     InstanceId=Config.INSTANCE_ID
    # )

    # routingProfiles = response['RoutingProfileSummaryList']

    # Get a list of the Arn for each routing profile
    routingProfilesArns = await cachedData.get('get_routingProfilesArns')


    # Get info for all the routing profiles
    response = client.get_current_user_data(
        InstanceId=Config.INSTANCE_ID,
        Filters={
            'RoutingProfiles': routingProfilesArns
        }
    )

    list = response['UserDataList']
    parsed = [models.AgentsDataListItem(
                                agentID=str(userData['User']['Id']), 
                                name= await cachedData.get('get_agent_name_data', id=userData['User']['Id']),
                                queue= await cachedData.get('get_routing_profile_name_data', id=userData['RoutingProfile']['Id']),
                                status= userData['Status']['StatusName'], 
                                requireHelp=userData['Status']['StatusName'] == "Needs Assistance", calls=5, rating=4.5) 
                                for userData in list]
    return parsed

cachedData.add("routing_profiles_data", routing_profiles_data, 20)

async def get_queue_description(queueID: str):
    client = boto3.client('connect')
    response = client.describe_queue(
        InstanceId=Config.INSTANCE_ID,
        QueueId=queueID
    )
    return response['Queue']

cachedData.add("get_queue_description", get_queue_description, 60*24) # 24 hours

async def get_queues_data():
    client = boto3.client('connect')
    response = client.list_queues(
        InstanceId=Config.INSTANCE_ID,
        QueueTypes=[
            'STANDARD',
        ]
    ) # get active queues

    builtData = []

    # get additional queue info
    for q in response['QueueSummaryList']:
        try:
            # metrics
            metric_data = client.get_current_metric_data(
                InstanceId=Config.INSTANCE_ID,
                Filters={
                    'Queues': [q['Id']],
                    'Channels': ['VOICE', 'CHAT']
                },
                CurrentMetrics=[
                    {
                        'Name': 'CONTACTS_IN_QUEUE',
                        'Unit': 'COUNT'
                    },
                    {
                        'Name': 'OLDEST_CONTACT_AGE',
                        'Unit': 'SECONDS'
                    }
                ],
                Groupings=[
                    'QUEUE'
                ],
                MaxResults=1
            )

            # Assuming successful retrieval, extract the metrics values
            contacts_in_queue = 0
            contact_age_average = 0  # Initialize the variable for the oldest contact age
            if metric_data['MetricResults']:
                for collection in metric_data['MetricResults'][0]['Collections']:
                    if collection['Metric']['Name'] == 'CONTACTS_IN_QUEUE':
                        contacts_in_queue = collection['Value']
                    elif collection['Metric']['Name'] == 'OLDEST_CONTACT_AGE':
                        contact_age_average += collection['Value']

            average_wait_time = contact_age_average / contacts_in_queue if contacts_in_queue > 0 else 0

            # queue info/description
            queue_data = await cachedData.get('get_queue_description', queueID=q['Id'])

            MaxContacts = int(queue_data.get('MaxContacts', 10) * 0.8) # 80% of the max contacts
            status = queue_data.get('Status', 'DISABLED')

        except (BotoCoreError, ClientError) as error:
            print(f"Error fetching current metric data: {error}")
            contacts_in_queue = 0  # Default/fallback value in case of error
            contact_age_average = 0  # Default/fallback value in case of error
            MaxContacts = 0
            status = 'DISABLED'
            average_wait_time = 0

        builtData.append(models.QueueDataListItem(
            queueID=q['Id'],
            name=q['Name'],
            maxContacts=MaxContacts,
            usage=contacts_in_queue / MaxContacts * 100 if MaxContacts > 0 else 0,
            enabled=status == "ENABLED",
            waiting=contacts_in_queue, 
            averageWaitTime=average_wait_time  
        ))

    return builtData

cachedData.add("get_queues_data", get_queues_data, 20)