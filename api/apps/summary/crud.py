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

async def getLatestAgentContact(agent_id: str) -> dict:
    client = boto3.client('connect')
    response = client.search_contacts(
        InstanceId=Config.INSTANCE_ID,
        TimeRange={
            'Type': 'CONNECTED_TO_AGENT_TIMESTAMP',
            'StartTime': datetime.now() - timedelta(days=30),
            'EndTime': datetime.now()
        },
        SearchCriteria={
            'AgentIds': [agent_id]
        },
        Sort={
            'FieldName': 'CONNECTED_TO_AGENT_TIMESTAMP',
            'Order': 'DESCENDING'
        },
        MaxResults=1
    )

    if len(response['Contacts']) == 0:
        return "<p>You do not have a recent contact. I will give you a recommendation once you do!<p>"

    return response['Contacts'][0]

cachedData.add('getLatestAgentContact', getLatestAgentContact, 120)

async def getLatestAgentTranscript(agent_id: str) -> str:
    contactData = await cachedData.get('getLatestAgentContact', agent_id=agent_id)
    contactID = contactData['Id']

    file =f'{contactID}_analysis_' 

    clients3 = boto3.client('s3')

    response = clients3.list_objects_v2(
        Bucket='amazon-connect-d62f5eebe090',
    )

    matches = [obj['Key'] for obj in response['Contents'] if file in obj['Key']]

    if len(matches) == 0:
        raise HTTPException(status_code=404, detail="Transcript not found")

    file = matches[0]

    response = clients3.get_object(
        Bucket='amazon-connect-d62f5eebe090',
        Key=file
    )

    return response['Body'].read().decode('utf-8')

cachedData.add('getLatestAgentTranscript', getLatestAgentTranscript, 120)

async def fetchRecommendations(agent_id: str) -> str:
    res = await cachedData.get('getLatestAgentTranscript', agent_id=agent_id)

    # call the gpt endpoint at localhost:8081/recommendations/{agent_id}
    request = requests.post(f'{Config.GPT_URI}recommendations/{agent_id}', data=res, headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {Config.GPT_Key}'})

    if request.status_code != 200:
        return "Sorry, I am not available at the moment. Please try again later."
    
    return request.text.strip('"').replace("\\n", "\n\n")

cachedData.add('fetchRecommendations', fetchRecommendations, 120)
