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