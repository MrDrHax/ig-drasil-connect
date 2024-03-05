from pydantic import BaseModel
from typing import List

from pydantic import BaseModel

class StartCallResponse(BaseModel):
    call_id: str
    message: str

class EndCallResponse(BaseModel):
    call_id: str
    message: str

class CreateContactResponse(BaseModel):
    contact_id: str
    contact_name: str
    phone_number: str

class CallDetailsResponse(BaseModel):
    call_id: str
    name: str
    number: str
    call_subject: str

class AgentAvailability(BaseModel):
    agent_id: str
    agent_name: str  
    availability: str
