from fastapi import APIRouter, Depends, HTTPException
from . import models, crud
from config import Config
from starlette.responses import RedirectResponse
from AAA.requireToken import oauthScheme

#Imports for Authentication in IAM Identity Center
import requests

import logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/extras", 
    tags=["extras"],
    responses = {
        200: {"description": "Success"},
        #202: {"description": "Accepted, request is being processed. Applies for connect requests that might take a while."},
        400: {"description": "Bad request, parameters are missing or invalid"},
        401: {"description": "Unauthorized. The request was not authorized."},
        404: {"description": "Not found"},
        500: {"description": "Internal server error, unknown error occurred."},
        503: {"description": "Service unavailable. Amazon Connect did not respond."},
    }
)

@router.post("/route/{callID}/{agentID}", tags=["connect"], responses={202: {"description": "Accepted, request is being processed. Continue on the connect app."}})
async def route_call(callID: int, agentID: int) -> str:
    '''
    Routes a call to a specific agent.
    '''
    return "success"

@router.get("/agentID", tags=["agents"])
async def get_agentID() -> str:
    '''
    Returns the agentID of the user.
    Works only for logged in users.
    '''
    return "1"

@router.get("/IAM", tags=["auth"])
async def get_IAM(deviceID: str) -> str:
    '''
    Returns the IAM link.
    Starts the IAM oauth process.
    '''
    # domain = Config.AUTH_DOMAIN + "protocol/openid-connect/authorize?response_type=code&client_id=" + Config.KEYCLOAK_ID + "&redirect_uri=" + Config.MY_DOMAIN + "extras/IAM/callback&scope=openid"
    domain = f"{Config.AUTH_DOMAIN}protocol/openid-connect/auth?response_type=code&client_id={Config.KEYCLOAK_ID}&redirect_uri={Config.MY_DOMAIN}extras/IAM/callback&scope=openid"
    return domain

@router.get("/apiToken", tags=["auth"])
async def get_apiToken() -> str:
    '''
    Returns the API token.
    '''
    return RedirectResponse(oauthScheme)

@router.get("/login", tags=["auth"])
async def get_IAM(redirect: str) -> str:
    '''
    Returns the IAM link.
    Starts the IAM oauth process.
    '''
    # domain = Config.AUTH_DOMAIN + "protocol/openid-connect/authorize?response_type=code&client_id=" + Config.KEYCLOAK_ID + "&redirect_uri=" + Config.MY_DOMAIN + "extras/IAM/callback&scope=openid"
    domain = f"{Config.AUTH_DOMAIN}protocol/openid-connect/auth?response_type=code&client_id={Config.KEYCLOAK_ID}&redirect_uri={redirect}&scope=openid"
    return domain

@router.get("/IAM/callback", tags=["auth"])
async def get_IAM_callback(code:str, redirect_uri:str) -> models.Token:
    '''
    Returns the IAM token.
    Finishes the IAM oauth process.

    Make sure to add the token to the user's session, and authenticate the user on next calls. Token type is bearer.
    '''
    #Endpoints
    authorization_endpoint = Config.AUTH_DOMAIN + "protocol/openid-connect/auth"
    token_endpoint = Config.AUTH_DOMAIN + "protocol/openid-connect/token"
    userInfo_endpoint = Config.AUTH_DOMAIN + "protocol/openid-connect/userinfo"

    # redirect_uri = Config.MY_DOMAIN + "extras/IAM/callback"

    #Create the request for the token
    parameters = {'grant_type' : 'authorization_code', 'code' : code, 'client_id' : Config.KEYCLOAK_ID, 'redirect_uri' : redirect_uri}
    req_headers = {'Content-Type' : 'application/x-www-form-urlencoded', 'Authorization' : 'Basic ' + Config.BASE64AUTH}
    r = requests.request('POST', url = token_endpoint, data = parameters, headers=req_headers, verify=False)
    #TODO: Add verification of the token with the keycloak certificate

    #Saves the info returned from the token Endpoint
    id_token = str(r.json().get("id_token", "NO ID TOKEN"))
    access_token = str(r.json().get("access_token", "NO ACCESS TOKEN"))
    refresh_token = str(r.json().get("refresh_token", "NO REFRESH TOKEN"))

    #Create the request for the user info
    r2 = requests.request('GET', url = userInfo_endpoint, headers= {'Authorization' : 'Bearer ' + access_token}, verify=False)

    #Get deviceID
    try:
        deviceID = str(r2.json().get("preferred_username", "NO DEVICE ID"))
    except:
        deviceID = "NO DEVICE ID"

    return models.Token(id_token= id_token, access_token= access_token, refresh= refresh_token, deviceID= deviceID)

@router.get("/IAM/refresh", tags=["auth"])
async def get_IAM_refresh(refresh: str, deviceID: str) -> models.Token:
    '''
    Returns the refreshed IAM token.

    Make sure to add the token to the user's session, and authenticate the user on next calls. Token type is bearer.
    '''

    # URL for the token endpoint
    token_endpoint = f"{Config.AUTH_DOMAIN}protocol/openid-connect/token"

    # Parameters for the request
    parameters = {
        'client_id': Config.KEYCLOAK_ID, 
        'refresh_token': refresh,
        'grant_type': 'refresh_token',
        'client_secret': Config.KEYCLOAK_SECRET,  # Only if your client is confidential
    }

    # Headers for the request
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Making the POST request to the token endpoint
    response = requests.post(token_endpoint, data=parameters, headers=headers, verify=False)

    if response.status_code == 200:
        # Parse the JSON response
        new_tokens = response.json()
        new_token = new_tokens.get('id_token')
        new_access_token = new_tokens.get('access_token')
        new_refresh_token = new_tokens.get('refresh_token', refresh)  # Use the old refresh token if a new one isn't provided
        
        # Return the new tokens
        return models.Token(id_token=new_token, access_token=new_access_token, refresh=new_refresh_token, deviceID=deviceID)
    else:
        # Handle error
        logger.error(f"Failed to refresh token: {response.text}")
        raise HTTPException(response.status_code, "Failed to refresh token")


@router.get("/AI/summary/{callID}", tags=["AI"])
async def get_AI_summary(callID: int) -> str:
    '''
    Returns a summary of the call, generated by AI.
    '''

    return "This is a test summary of the call."

@router.get("/AI/transcript/{callID}", tags=["AI"])
async def get_AI_transcript(callID: int) -> str:
    '''
    Returns a transcript of the call, generated by AI.
    '''

    return "This is a test transcript of the call."

@router.get("/AI/sentiment/{callID}", tags=["AI"])
async def get_AI_sentiment(callID: int) -> str:
    '''
    Returns the sentiment of the call, generated by AI.
    '''

    return "This is a test sentiment of the call."

@router.get("/lex/QA", tags=["lex"])
async def get_lex() -> list[str]:
    '''
    Returns questions to ask when the user is using the Lex QA service.
    '''

    return ["How did the call go?", "Was the agent helpful?", "Would you like to leave a comment?"]

@router.post("/lex/QA", tags=["lex"])
async def post_lex(answers: list[str], questions: list[str]) -> str:
    '''
    Processes the QA answers from the user.
    '''

    return "Thank you for your feedback."
