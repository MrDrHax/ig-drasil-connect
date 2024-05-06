from fastapi import Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer
from config import Config
from starlette.middleware.base import BaseHTTPMiddleware
from AAA.userType import testToken

import logging
logger = logging.getLogger(__name__)

oauthScheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{Config.AUTH_DOMAIN}protocol/openid-connect/auth",
    tokenUrl=f"{Config.AUTH_DOMAIN}protocol/openid-connect/token",
    refreshUrl=f"{Config.AUTH_DOMAIN}protocol/openid-connect/refresh",
    scopes={
        "openid": "Access to the user's OpenID profile",
        "manager": "Access to the manager's profile",
        "agent": "Access to the agent's profile",
    },
)

requireToken = oauthScheme #OAuth2PasswordBearer(oauthScheme)

def isTokenExpired(token: str):
    return testToken(token) == None


def refreshAccessToken(refresh_token: str):
    # TODO implement this for automatic token refresh
    return refresh_token

class TokenRefreshMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = Response("Internal server error", status_code=500)
        try:
            # Check if the access token has expired
            # TODO: Fix this to check for the token in the header
            if 'access_token' in request.cookies and 'refresh_token' in request.cookies:
                access_token = request.cookies['access_token']
                refresh_token = request.cookies['refresh_token']
                # If the access token has expired, refresh it
                if isTokenExpired(access_token):
                    access_token = refreshAccessToken(refresh_token)
                    request.cookies['access_token'] = access_token
                response = await call_next(request)
            else:
                logger.warning(f"No access token found in the request: {request.url.path}")
                response = await call_next(request)
        except Exception as e:
            logger.error(f"Error in TokenRefreshMiddleware: {e}")
        return response