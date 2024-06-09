from sqlalchemy.orm import Session
from . import models
import boto3
from config import Config
from cache.cache_object import cachedData

import logging
logger = logging.getLogger(__name__)

async def get_agent_id(username: str) -> str:
    client = boto3.client('connect')
    response = client.list_users(
        InstanceId=Config.INSTANCE_ID
    )

    for user in response['UserSummaryList']:
        #logger.info(user['Username'])
        if user['Username'].lower() == username.lower():
            return user['Id']

    return "Does not exist"

cachedData.add('get_agent_id', get_agent_id, 60*60*24 ) # 1 day