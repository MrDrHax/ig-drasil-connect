from fastapi import APIRouter
from DocumentDB.DB.Atlas_integration_test import client
import boto3
from config import Config

import logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix = '/Endpoints',
    responses={
        200: {"description": "Success"},
        400: {"description": "Bad request, parameters are missing or invalid"},
        401: {"description": "Unauthorized. The request was not authorized."},
        404: {"description": "Not found"},
        500: {"description": "Internal server error, unknown error occurred."},
        503: {"description": "Service unavailable. Amazon Connect did not respond."},
    }
)

#We get the call contact lens analysis info ans save in our Atlas MongoDB
@router.get("/call-information-analysis",response_model=dict)
async def ListRealTimeContactAnalysisSegment():
        db = client['IGDrasilTest']
        collection = db['Test1']
        aws = boto3.client('connect')
        response = aws.list_realtime_contact_analysis_segments(
                    InstanceId = Config.INSTANCE_ID,
                    ContactId='e6f4e310-d413-440f-8b94-1f967dfce418'
        )
        result = collection.insert_one(response)
        return {"Insert_id": str(result.inserted_id)}