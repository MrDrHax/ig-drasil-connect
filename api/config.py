import os
from dotenv import load_dotenv

import logging
logger = logging.getLogger(__name__)

# Determine if we're running on an Ubuntu server
if os.name == 'posix' and os.uname().release == 'ubuntu':
    load_dotenv('.env')
else:
    load_dotenv('.dev.env')

# if you want to add a config variable, add it here!!!
class Config:
    PORT = os.getenv('PORT', 8080)
    '''The port the server will run on.'''
    HOST = os.getenv('HOST', 'localhost')
    '''The host the server will run on.'''
    DEBUG = os.getenv('DEBUG', False)
    '''is the server running in debug mode?'''
    AUTH_DOMAIN = os.getenv('AUTH_DOMAIN', '>_<')
    '''The domain of keycloak, used for authentication. Includes a finalizing "/"'''
    BASE64AUTH = os.getenv('BASE64AUTH', '>_<')
    '''The base64 encoded client_id:client_secret for keycloak.'''
    MY_DOMAIN = os.getenv('MY_DOMAIN', 'http://localhost:8080/')
    '''The domain of the server.'''
    KEYCLOAK_ID = os.getenv('KEYCLOAK_ID', '>_<')
    '''The client_id for keycloak.'''
    KEYCLOAK_SECRET = os.getenv('KEYCLOAK_SECRET', '>_<')
    '''The client_secret for keycloak.'''
    INSTANCE_ID = os.getenv('INSTANCE_ID', '>_<')
    '''AWS Connect instance ID.'''


def logConfig():
    config = "Configuration:\n"

    for key, value in Config.__dict__.items():
        if key.isupper():
            config += f"{key}: {value}\n"

    logger.debug(config)