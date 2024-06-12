from fastapi import APIRouter, Depends, HTTPException
from typing import List
from config import Config
from typing import Annotated
from AAA.requireToken import requireToken
import AAA.userType as userType
from cache.cache_object import cachedData

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
    
    user_id = await get_agentID(username=userType.getUserName(token), token=token)

    client = boto3.client('connect')

    # Get the id for the call
    response = client.get_current_user_data(
        InstanceId=Config.INSTANCE_ID,
        Filters={
            'Agents': [ agent_id ]      
        }
    )

    if len(response['UserDataList'][0]['Contacts']) == 0:
        raise HTTPException(status_code=404, detail="No contact found for the agent.")
    
    call_id = response['UserDataList'][0]['Contacts'][0]['ContactId']

    response = client.monitor_contact(
        InstanceId=Config.INSTANCE_ID,
        ContactId=call_id,
        UserId=user_id,
        AllowedMonitorCapabilities=['BARGE', 'SILENT_MONITOR']
    )
    return user_id

@router.post("/change_status")
async def change_status(token: Annotated[str, Depends(requireToken)], agent_id: str, status: str):
    """
    Change the status of an agent.

    @param agent_id: ID of the agent whose status to change.
    @param status: New status of the agent.

    @return: Confirmation message of the status change.
    """
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")
    
    response = await cachedData.get('list_statuses')
    
    statusID = None

    for statuses in response:
        if statuses['Name'] == status:
            statusID = statuses['AgentStatusId']

    if statusID == None:
        raise HTTPException(status_code=400, detail="Invalid status.")
    
    client = boto3.client('connect')
    response = client.put_user_status(
        InstanceId=Config.INSTANCE_ID,
        AgentStatusId=statusID,
        UserId=agent_id
    )

    return {"message": "Status changed"}

@router.post("/change_routing_profile")
async def change_routing_profile(token: Annotated[str, Depends(requireToken)], agent_id: str, routing_profile_name: str):
    """
    Change the routing profile of an agent.

    @param agent_id: ID of the agent whose routing profile to change.
    @param routing_profile: New routing profile of the agent.

    @return: Confirmation message of the routing profile change.
    """
    if not userType.isManager(token):
        raise HTTPException(status_code=401, detail="Unauthorized. You must be a manager to access this resource.")
    
    response = await cachedData.get('get_routing_profile_list')

    for profile in response:
        if profile['Name'] == routing_profile_name:
            routing_profile_id = profile['Id']

    if routing_profile_id == None:
        raise HTTPException(status_code=400, detail="Invalid routing profile.")
    
    client = boto3.client('connect')
    response = client.update_user_routing_profile(
        InstanceId=Config.INSTANCE_ID,
        UserId= agent_id,
        RoutingProfileId=routing_profile_id
    )

    return {"message": "Routing profile changed"}