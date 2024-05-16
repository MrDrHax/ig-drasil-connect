from sqlalchemy.orm import Session
from . import models
import boto3
from config import Config
from cache.cache_object import cachedData

import logging
logger = logging.getLogger(__name__)

def agent_profile_data(id) -> tuple:
    client = boto3.client('connect')
    response = client.describe_user(
        InstanceId=Config.INSTANCE_ID,
        UserId=id
    )

    FullName = f'{response["User"]["IdentityInfo"]["FirstName"]} {response["User"]["IdentityInfo"]["LastName"]}'
    Agent_email = response["User"]["Username"]

    try:
        Agent_mobile = response["User"]["IdentityInfo"]["Mobile"]
    except:
        Agent_mobile = "Unknown"

    return FullName, Agent_email, Agent_mobile

cachedData.add("agent_profile_data", agent_profile_data)

def check_agent_availability_data():
    client = boto3.client('connect')

    # Get info for the first routing profile
    response = client.get_current_metric_data(
        InstanceId=Config.INSTANCE_ID,
        Filters={
            'RoutingProfiles': [
                '69e4c000-1473-42aa-9596-2e99fbd890e7',
            ]
        },
        CurrentMetrics=[
            {
                'Name': 'AGENTS_ONLINE',
                'Unit': 'COUNT'
            },
        ]
    )

    toIterate = response['MetricResults'][0]['Collections']
    # return toIterate
    toReturn = [(i['Metric']['Name'], i['Value']) for i in toIterate]

    return toReturn

cachedData.add("check_agent_availability_data", check_agent_availability_data, 10)