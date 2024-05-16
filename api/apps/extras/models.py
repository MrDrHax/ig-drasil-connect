from pydantic import BaseModel

import logging
logger = logging.getLogger(__name__)

# Define your models here. For example:
class Extra(BaseModel):
    id: int
    name: str
    description: str

# If there are no models for the 'extras' app, this file can be left blank.
# This is intentionally left blank.
    
class Token(BaseModel):
    id_token: str
    access_token: str
    refresh: str
    deviceID: str