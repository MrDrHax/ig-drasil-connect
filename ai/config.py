
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

def logConfig():
    config = "Configuration:\n"

    for key, value in Config.__dict__.items():
        if key.isupper():
            config += f"{key}: {value}\n"

    logger.debug(config)