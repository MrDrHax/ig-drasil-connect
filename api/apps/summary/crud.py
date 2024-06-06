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

#LATEST TRANSCRIPT

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

# AGENT RATINGS

async def getAllAgentContact(agent_id: str) -> list[dict]:
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
        MaxResults=100
    )

    if len(response['Contacts']) == 0:
        return "<p>You do not have a recent contact.<p>"

    return response['Contacts']

cachedData.add('getAllAgentContact', getAllAgentContact, 120)

def calculateRating(data: json) -> int:
    # Extract relevant data
    try:
        agent_sentiment = data["ConversationCharacteristics"]["Sentiment"]["OverallSentiment"]["AGENT"]
    except:
        agent_sentiment = 0
    try:
        customer_sentiment = data["ConversationCharacteristics"]["Sentiment"]["OverallSentiment"]["CUSTOMER"]
    except:
        customer_sentiment = 0
    
    interruptions_count = data["ConversationCharacteristics"]["Interruptions"]["TotalCount"]
    interruptions_time = data["ConversationCharacteristics"]["Interruptions"]["TotalTimeMillis"]
    agent_talk_time = data["ConversationCharacteristics"]["TalkTime"]["DetailsByParticipant"]["AGENT"]["TotalTimeMillis"]
    customer_talk_time = data["ConversationCharacteristics"]["TalkTime"]["DetailsByParticipant"]["CUSTOMER"]["TotalTimeMillis"]
    non_talk_time = data["ConversationCharacteristics"]["NonTalkTime"]["TotalTimeMillis"]
    total_conversation_time = data["ConversationCharacteristics"]["TotalConversationDurationMillis"]

    # Normalize sentiment scores (Assuming sentiment score range is -5 to 5)
    agent_sentiment_normalized = (agent_sentiment + 5) / 10
    customer_sentiment_normalized = (customer_sentiment + 5) / 10

    # Normalize interruptions (Assuming a high number of interruptions is bad, so inversely scale it)
    max_interruptions = 10  # Assuming 10 as a threshold for many interruptions
    interruptions_normalized = 1 - min(interruptions_count / max_interruptions, 1)

    # Normalize interruptions time (Assuming interruptions time is high, so inversely scale it)
    interruptions_time_normalized = 1 - min(interruptions_time / total_conversation_time, 1)

    # Normalize non-talk time (Assuming higher non-talk time is bad, so inversely scale it)
    non_talk_time_normalized = 1 - min(non_talk_time / total_conversation_time, 1)

    # Normalize talk time balance (Ideal talk time balance is 50-50, so we take the difference and scale it)
    talk_time_difference = abs(agent_talk_time - customer_talk_time) / total_conversation_time
    talk_time_normalized = 1 - min(talk_time_difference * 2, 1)

    # Combine all normalized scores to calculate the final rating
    final_score = (agent_sentiment_normalized + customer_sentiment_normalized + 
                   interruptions_normalized + interruptions_time_normalized + non_talk_time_normalized + 
                   talk_time_normalized) / 6

    # Scale final score to 0-5
    final_rating = final_score * 5
    
    return round(final_rating, 2)

async def getListAgentRatings(agent_id: str) -> list[models.AgentRating]:
    contactData = await cachedData.get('getAllAgentContact', agent_id=agent_id)

    clients3 = boto3.client('s3')

    objects = clients3.list_objects_v2(
        Bucket='amazon-connect-d62f5eebe090',
    )

    agent_ratings = []

    for contact in contactData:
        contactID = contact['Id']

        file =f'{contactID}_analysis_' 

        matches = [obj['Key'] for obj in objects['Contents'] if file in obj['Key']]

        if len(matches) == 0:
            raise HTTPException(status_code=404, detail="Transcript not found")

        file = matches[0]

        response = clients3.get_object(
            Bucket='amazon-connect-d62f5eebe090',
            Key=file
        )

        transcript = response['Body'].read().decode('utf-8')

        transcript = json.loads(transcript)

        # Filter out short conversations (less than 10 seconds)
        if transcript['ConversationCharacteristics']['TotalConversationDurationMillis'] > 100:
            agent_ratings.append(models.AgentRating(rating=calculateRating(transcript), timestamp=contact['InitiationTimestamp']))

    return agent_ratings

cachedData.add('getListAgentRatings', getListAgentRatings, 120)

async def getListContactParsed(agent_id: str) -> list[models.AgentContactProfile]:
    contactData = await cachedData.get('getAllAgentContact', agent_id=agent_id)

    clients3 = boto3.client('s3')

    objects = clients3.list_objects_v2(
        Bucket='amazon-connect-d62f5eebe090',
    )

    parsed_contacts = []

    for contact in contactData:
        contactID = contact['Id']

        file =f'{contactID}_analysis_' 

        matches = [obj['Key'] for obj in objects['Contents'] if file in obj['Key']]

        if len(matches) == 0:
            raise HTTPException(status_code=404, detail="Transcript not found")

        file = matches[0]

        response = clients3.get_object(
            Bucket='amazon-connect-d62f5eebe090',
            Key=file
        )

        transcript = response['Body'].read().decode('utf-8')

        transcript = json.loads(transcript)

        # Filter out short conversations (less than 10 seconds)
        if transcript['ConversationCharacteristics']['TotalConversationDurationMillis'] > 100:
            # Try to get summary
            try:
                summary = transcript['ConversationCharacteristics']['ContactSummary']['PostContactSummary']['Content']
            except:
                summary = "No summary found."
            # Try to get sentiment
            try:
                sentiment = transcript['ConversationCharacteristics']['Sentiment']['OverallSentiment']['AGENT']
                c_sentiment = transcript['ConversationCharacteristics']['Sentiment']['OverallSentiment']['CUSTOMER']
            except:
                sentiment = 0.0
                c_sentiment = 0.0
            parsed_contacts.append(models.AgentContactProfile(summary=summary,status=transcript['JobStatus'], duration=transcript['ConversationCharacteristics']['TotalConversationDurationMillis'], agentSentiment=sentiment, customerSentiment=c_sentiment , timestamp=contact['InitiationTimestamp'].strftime("%m-%d %H:%M")))

    return parsed_contacts

cachedData.add('getListContactParsed', getListContactParsed, 120)