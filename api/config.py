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
    PORT = int(os.getenv('PORT', 8080))
    '''The port the server will run on.'''
    HOST = os.getenv('HOST', 'localhost')
    '''The host the server will run on.'''
    DEBUG = os.getenv('DEBUG', False) in ['True', 'true', '1', 'yes', 'Yes', 'Y', 'y']
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
    '''AWS Connect instance ID. '''
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', '>_<')
    '''AWS S3 bucket name. '''
    URI_MONGODB = os.getenv('URI_MONGODB','UwU')
    '''The URI for the mongodb connection. '''
    IDENTITY_STORE_ID = os.getenv('IDENTITY_STORE_ID', '>_<')
    '''AWS SSO Instance ID. '''
    KEYCLOAK_URI = os.getenv('KEYCLOAK_URI', 'https://localhost:8443/')
    '''The URI for keycloak'''
    GPT_URI = os.getenv('GPT_URI', 'http://localhost:8081/')
    '''The URI for the GPT endpoint'''
    GPT_Key = os.getenv('GPT_Key', '1234')
    '''The key for the GPT endpoint'''


def logConfig():
    config = "Configuration:\n"

    for key, value in Config.__dict__.items():
        if key.isupper():
            config += f"{key}: {value}\n"

    logger.debug(config)
