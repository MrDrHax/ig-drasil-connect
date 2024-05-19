from pydantic import BaseModel
from datetime import datetime
from typing import List

class AgentNote(BaseModel):
    id_agent:str
    date:datetime
    notes:List[dict]

class SupervisorAgent(BaseModel):
    id_agent: str
    id_supervisor: str
    messages: List[dict]
