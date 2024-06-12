import boto3
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from config import Config
from MongoAtlas.DB_connection import DataBase
from . import models

from apps.extras.endpoints import get_agentID

from typing import Annotated
from AAA.requireToken import requireToken
import AAA.userType as userType

from datetime import datetime, timezone
from base64 import b64encode, b64decode


from cache.cache_object import cachedData
import logging
logger = logging.getLogger(__name__)

db_instance = DataBase.get_instance()
db = db_instance.get_database()

router = APIRouter(
    prefix="/MongoAtlas",
    tags=["actions"],
    responses={
        200: {"description": "Success"},
        400: {"description": "Bad request, parameters are missing or invalid"},
        401: {"description": "Unauthorized. The request was not authorized."},
        404: {"description": "Not found"},
        500: {"description": "Internal server error, unknown error occurred."},
        503: {"description": "Service unavailable. Amazon Connect did not respond."},
    }
)

#Example1 get from contact lens endpoint
@router.get('/contact-analysis-segment',response_model=List[dict])
async def get_contact_lens():
    """
    Description:
    Provides a list of analysis segments for a real-time analysis session.
    
    Parameters:
    INSTANCEID: The identifier of the Amazon Connect instance.
    CONTACTID: The identifier of the contact.
    """
    client = boto3.client('connect')
    response = client.list_realtime_contact_analysis(
        InstanceId = Config.INSTANCEID,
        ContactId = 'e6f4e310-d413-440f-8b94-1f967dfce418'
    )
    col = db['Test1']
    col.insert_one(response)
    return response

#Chat endpoints

@router.get('/get_chat_by_id', tags=["DB"])
async def get_chat_by_id(token: Annotated[str, Depends(requireToken)], agent_id: str) -> List[models.ChatMessageBody]:
    """
    Returns all chats from a specific agent ID.
    """
    if not userType.isManager(token) and not userType.isAgent(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager or an agent to access this resource.")
    
#    return db['chats'].find_one({"agent_id": agent_id})

    if agent_id == None:
        agent_id = await get_agentID(token)

    try:
        chat = db['chats'].find_one({"agent_id": agent_id})

        for index, message in enumerate(chat['messages']):
            # Decode the base64-encoded string
            chat['messages'][index]['content'] = b64decode(message['content']).decode('utf-8').split(Config.BASE64AUTH)[0]
            # Convert the timestamp to local timezone
            chat['messages'][index]['timestamp'] = message['timestamp'].replace(tzinfo=timezone.utc).astimezone(tz=None)

        return chat['messages']

    except Exception as e:
        logger.error(e)
        return []

@router.get('/get_chat', tags=["DB"])
async def get_chat(token: Annotated[str, Depends(requireToken)]) -> List[models.ChatMessage]:
    """
    Returns a list of all chats.
    """    

    if not userType.isManager(token) and not userType.isAgent(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager or an agent to access this resource.")
    
    return db['chats'].find()

@router.post('/post_chat', tags=["DB"])
async def post_chat(token: Annotated[str, Depends(requireToken)], message: str, agent_id: str, supervisor: bool) -> str:
    """
    Posts a chat message.
    """
    if not userType.isManager(token) and not userType.isAgent(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager or an agent to access this resource.")
    
    salted_message = message + Config.BASE64AUTH + agent_id
    encoded_message = b64encode(salted_message.encode('utf-8'))
    #logger.info(b64decode(encoded_message).decode('utf-8'))
    db['chats'].update_one({"agent_id": agent_id}, {"$push": {"messages": {"content": encoded_message, "supervisor_sender": supervisor, "timestamp": datetime.now(tz=timezone.utc)}}}, upsert=True)

    return "success"

async def getAllRatings():
    return db['SurveyResults'].find()
cachedData.add('getAllRatings', getAllRatings, 120) # 2 minutes

async def get_specific_rating(contact_id: str):
    all_contacts = await cachedData.get('getAllRatings')

    return list(filter(lambda contact: contact['contactId'] == contact_id, all_contacts))
cachedData.add('get_specific_rating', get_specific_rating, 60 * 60 * 24) # 24 hours

@router.get('/get_ratings', tags=["DB"])
async def get_ratings(token: Annotated[str, Depends(requireToken)], contact_id: str) -> List[models.Ratings]:
    """
    Returns the rating from a specific contact ID.
    """
    if not userType.isManager(token) and not userType.isAgent(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager or an agent to access this resource.")
    
    return await cachedData.get('get_specific_rating', contact_id)