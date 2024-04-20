from fastapi import APIRouter, Depends
from . import models, crud
from config import Config

#Imports for Authentication in IAM Identity Center
import requests

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
    domain = Config.MY_DOMAIN + "protocol/openid-connect/authorize?response_type=code&client_id=" + Config.KEYCLOAK_ID + "&redirect_uri=" + Config.MY_DOMAIN + "extras/IAM/callback&scope=openid"
    return domain
 
@router.get("/IAM/callback", tags=["auth"])
async def get_IAM_callback(code:str) -> models.Token:
    '''
    Returns the IAM token.
    Finishes the IAM oauth process.

    Make sure to add the token to the user's session, and authenticate the user on next calls. Token type is bearer.
    '''
    #Endpoints
    authorization_endpoint = Config.AUTH_DOMAIN + "protocol/openid-connect/auth"
    token_endpoint = Config.AUTH_DOMAIN + "protocol/openid-connect/token"
    userInfo_endpoint = Config.AUTH_DOMAIN + "protocol/openid-connect/userinfo"

    redirect_uri = Config.MY_DOMAIN + "extras/IAM/callback"

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

    return models.Token(id_token="example_token", access_token="example_access_token", refresh="example_refresh", deviceID="example_deviceID")

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
