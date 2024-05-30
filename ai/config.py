
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
    PORT = int(os.getenv('PORT', 8081))
    '''The port the server will run on.'''
    HOST = os.getenv('HOST', 'localhost')
    '''The host the server will run on.'''
    DEBUG = os.getenv('DEBUG', False).lower() in ['true', '1', 't', 'y', 'yes']
    '''is the server running in debug mode?'''
    DEVICE = os.getenv('DEVICE', 'cpu')
    '''What device should the model run on? gpu/cpu (can be amd, intel or cuda for specific gpu)'''
    GPTMODEL = os.getenv('GPTMODEL', 'orca-mini-3b-gguf2-q4_0.gguf')
    '''The model to use for generating responses.'''
    DOWNLOADGPT = os.getenv('DOWNLOADGPT', True).lower() in ['true', '1', 't', 'y', 'yes']
    '''Should the model be downloaded?'''
    SECRET = os.getenv('SECRET', '123')
    '''The secret key for the API server.'''

def logConfig():
    config = "Configuration:\n"

    for key, value in Config.__dict__.items():
        if key.isupper():
            config += f"{key}: {value}\n"

    logger.debug(config)