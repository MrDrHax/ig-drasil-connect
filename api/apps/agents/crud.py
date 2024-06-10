from fastapi import HTTPException
import markdown
import requests
from sqlalchemy.orm import Session
from . import models
import boto3
from datetime import datetime, timedelta
from cache.cache_object import cachedData
import json

from config import Config

import logging
logger = logging.getLogger(__name__)

async def getListAgentStatuses() -> dict:
    client = boto3.client('connect')
    resp = client.list_agent_statuses(
        InstanceId=Config.INSTANCE_ID
    )

    return resp['AgentStatusSummaryList']

cachedData.add('getListAgentStatuses', getListAgentStatuses, 86400) # 24 hours

async def get_current_user_data() -> dict:
    client = boto3.client('connect')
    users = client.list_users(
        InstanceId=Config.INSTANCE_ID,
    )
    userList = []
    for user in users['UserSummaryList']:
        userList.append(user['Id'])

    users_data = client.get_current_user_data(
        InstanceId=Config.INSTANCE_ID,
        Filters = {
            'Agents': userList
        }
    )

    return users_data

cachedData.add('get_current_user_data', get_current_user_data, 30) # 30 seconds