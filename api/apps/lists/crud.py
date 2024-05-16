from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models
import boto3
from config import Config
from cache.cache_object import cachedData

import logging
logger = logging.getLogger(__name__)

def routing_profiles_data() -> tuple:
    client = boto3.client('connect')
    # Get info for all the routing profiles
    response = client.get_current_user_data(
        InstanceId=Config.INSTANCE_ID,
        Filters={
            'RoutingProfiles': routingProfilesArns
        }
    )
    
    routingProfiles = response['RoutingProfileSummaryList']

    # Get a list of the Arn for each routing profile
    routingProfilesArns = [profile['Arn'] for profile in routingProfiles]

    list = response['UserDataList']
    parsed = [models.AgentsDataListItem(
                                agentID=str(userData['User']['Id']), 
                                name= client.get_agent_name(userData['User']['Id']),
                                queue= client.get_routing_profile_name(userData['RoutingProfile']['Id'], routingProfiles),
                                status= userData['Status']['StatusName'], 
                                requireHelp=userData['Status']['StatusName'] == "Needs Assistance", calls=5, rating=4.5) 
                                for userData in list]
    return parsed

cachedData.add("routing_profiles_data", routing_profiles_data, 60)
