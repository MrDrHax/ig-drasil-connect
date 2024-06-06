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
    
    title : str = Field("Last Contact Sentiment rating and Agent rating", example="Last Contact Sentiment rating and Agent rating", description="Last Contact Sentiment rating and Agent rating. In JSON format.")
    sentimentTitle: str = Field("Customer sentiment rating", example="Agent sentiment rating", description="Agent sentiment rating. In JSON format.")
    sentiment : float = Field(0.0, example=0.0, description="The sentiment of the agent. Higher is better. Uses KPIs to try to approach how well it's going", min=0, max=1)
    ratingTitle: str = Field("Agent rating", example="Agent rating", description="Agent rating. In JSON format.")
    rating: float = Field(5, example=5, description="The rating of the agent. Higher is better. Uses KPIs to try to approach how well it's going", min=0, max=5)
