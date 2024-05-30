from fastapi import APIRouter, Depends, HTTPException
from typing import List
from config import Config
from typing import Annotated
from AAA.requireToken import requireToken
import AAA.userType as userType

from apps.extras.endpoints import get_agentID

import boto3

import logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/actions",
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

@router.post("/join-call")
async def join_call(token: Annotated[str, Depends(requireToken)], agent_id: str):
    """
    Join a phone call in Amazon Connect.

    @param agent_id: ID of the agent whose call to join.

    @return: Confirmation message of the call joining.
    """
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")
    
    client = boto3.client('connect')

    response = client.get_current_user_data(
        InstanceId=Config.INSTANCE_ID,
        Filters={
            'Agents': [ agent_id ]      
        }
    )

    call_id = response['UserDataList'][0]['Contacts'][0]['ContactId']

    user_id = get_agentID(userType.getUserName(token))

    response = client.monitor_call(
        InstanceId=Config.INSTANCE_ID,
        ContactId=call_id,
        UserId=user_id,
        AllowedMonitorCapabilities=['BARGE']
    )

    return {"message": f"Call Joined: {call_id}"}

@router.post("/start-call")
async def start_call( phone_number: str):
    """
    start of a phone call in Amazon Connect.

    @param phone_number: Phone number to call.

    @return: Confirmation message of the call starting.
    """
    return {"message": f"Call Started: {phone_number}"}


@router.post("/end-call")
async def end_call(call_id: str):
    """
    end of a phone call in Amazon Connect.

    @param call_id: ID of the call that has ended.

    @return: Confirmation message of the call ending.
    """
    return {"message": f"Call Ended: {call_id}"}


@router.post("/create-contact")
async def create_contact(contact_name: str, phone_number: str):
    """
    Create a contact in Amazon Connect.

    @param contact_name: Name of the contact.
    @param phone_number: Phone number of the contact.

    @return: Details of the created contact.
    """
    return {"contact_name": contact_name, "phone_number": phone_number}



@router.get("/calls-details/{call_id}")
async def get_call_details(call_id: str):
    """
    Get details of a call in Amazon Connect.

    @param call_id: ID of the call to get details for.

    @return: Details of the specified call.
    """
    return {
        "call_id": call_id,
        "name": "Jane Doe",
        "number": "5521457834",
        "call_subject": "product information"
    }


@router.get("/agent-availability", response_model=List[dict])
async def check_agent_availability():
    """
    Verifies the availability of agents in Amazon Connect.

    @return 
        List containing the availability status of agents.
    """

    client = boto3.client('connect')

    # Get info for the first routing profile
    response = client.get_current_user_data(
        InstanceId=Config.INSTANCE_ID,
        Filters={
            'RoutingProfiles': [
                '69e4c000-1473-42aa-9596-2e99fbd890e7',
            ]
        }
    )

    #agents_availability = [
    #    {"agent_id": "123", "availability": "Available"},
    #    {"agent_id": "456", "availability": "Unavailable"},
    #    {"agent_id": "789", "availability": "Available"},
    #]
    return response['UserDataList']