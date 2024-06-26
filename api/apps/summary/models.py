from pydantic import BaseModel, Field

from datetime import datetime

import logging
logger = logging.getLogger(__name__)

class Summary(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True

class AgentTranscriptSummary(BaseModel):
    agent_id: str
    content: str = Field("Agent transcript summary", example="Agent transcript summary", description="Agent transcript summary. In JSON format.")

    class Config:
        from_attributes = True

class AgentPerformanceSummary(BaseModel):
    agent_id: str
    content: str = Field("Agent performance summary", example="Agent performance summary", description="Agent performance summary. In HTML format.")
    channel: str = Field("email", example="email", description="The channel for which the summary is generated")
    sentiment: float = Field(0.0, example=0.0, description="The sentiment of the agent. Higher is better. Uses KPIs to try to approach how well it's going", min=0, max=1)
    rating: float = Field(5, example=5, description="The rating of the agent. Higher is better. Uses KPIs to try to approach how well it's going", min=0, max=5) 
    

    class Config:
        from_attributes = True

class AgentRating(BaseModel):
    rating: float = Field(5, example=5, description="The rating of the agent. Higher is better. Uses KPIs to try to approach how well it's going", min=0, max=5)
    timestamp: datetime = Field(datetime.now(), example=datetime.now(), description="The timestamp of when the rating was given")

class AgentSentimentRating(BaseModel):
    
    
    sentiment : float = Field(0.0, example=0.0, description="The sentiment of the agent. Higher is better. Uses KPIs to try to approach how well it's going", min=0, max=1)
    rating: float = Field(5, example=5, description="The rating of the agent. Higher is better. Uses KPIs to try to approach how well it's going", min=0, max=5)
    recommendation: str = Field("You should try to have a nicer tone", example="You should try to have a nicer tone", description="The recommendation for the agent.")

class AgentContactProfile(BaseModel):
    summary: str = Field("Contact summary", example="Contact summary", description="Contact summary.")
    status: str = Field("No status", example="COMPLETED", description="The final status of the contact.")
    duration: int = Field(0, example=0, description="The duration of the contact in milliseconds.")
    agentSentiment: float = Field(0, example=5, description="The sentiment of the agent. Higher is better. Uses KPIs to try to approach how well it's going", min=0, max=5)
    customerSentiment: float = Field(0, example=5, description="The sentiment of the customer. Higher is better. Uses KPIs to try to approach how well it's going", min=0, max=5)
    timestamp: str = Field("%m-%d %H:%M", example="%m-%d %H:%M", description="The timestamp of when the contact was given")
    
class AgentTranscript(BaseModel):
    content: str = Field("Agent transcript", example="Agent transcript", description="Agent transcript. In JSON format.")

    class Config:
        from_attributes = True

