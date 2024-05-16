from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models
import boto3
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
