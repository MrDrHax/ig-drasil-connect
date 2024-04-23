import os
from dotenv import load_dotenv

# Determine if we're running on an Ubuntu server
if os.name == 'posix' and os.uname().release == 'ubuntu':
    load_dotenv('.env')
else:
    load_dotenv('.dev.env')

# if you want to add a config variable, add it here!!!
class Config:
    PORT = os.getenv('PORT', 8080)
    HOST = os.getenv('HOST', 'localhost')
    DEBUG = os.getenv('DEBUG', False)
    AUTH_DOMAIN = os.getenv('AUTH_DOMAIN', '>_<')
    BASE64AUTH = os.getenv('BASE64AUTH', '>_<')
    MY_DOMAIN = os.getenv('MY_DOMAIN', 'http://localhost:8080/')
    KEYCLOAK_ID = os.getenv('KEYCLOAK_ID', '>_<')
    INSTANCE_ID = os.getenv('INSTANCE_ID', '>_<')