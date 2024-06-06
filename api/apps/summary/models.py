from pydantic import BaseModel, Field

import logging
logger = logging.getLogger(__name__)

class Summary(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True

class AgentPerformanceSummary(BaseModel):
    agent_id: str
    content: str = Field("Agent performance summary", example="Agent performance summary", description="Agent performance summary. In HTML format.")

    class Config:
        from_attributes = True

class AgentTranscriptSummary(BaseModel):
    agent_id: str
    content: str = Field("Agent transcript summary", example="Agent transcript summary", description="Agent transcript summary. In HTML format.")

    class Config:
        from_attributes = True