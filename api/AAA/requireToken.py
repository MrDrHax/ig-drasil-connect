from fastapi.security import OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer
from config import Config

oauthScheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{Config.AUTH_DOMAIN}protocol/openid-connect/auth",
    tokenUrl=f"{Config.AUTH_DOMAIN}protocol/openid-connect/token",
    refreshUrl=f"{Config.AUTH_DOMAIN}protocol/openid-connect/refresh",
    scopes={"openid": "Access to the user's OpenID profile"},
)

requireToken = oauthScheme #OAuth2PasswordBearer(oauthScheme)

