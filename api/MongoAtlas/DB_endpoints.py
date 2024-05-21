import boto3
from typing import List
from fastapi import APIRouter
from config import Config
from MongoAtlas.DB_connection import DataBase

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

