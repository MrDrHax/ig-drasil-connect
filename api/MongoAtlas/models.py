from pydantic import BaseModel, Field
from datetime import datetime

import logging
logger = logging.getLogger(__name__)

class ChatMessageBody(BaseModel):
    content: str = Field("This is a test message", examples=["This is a test message", "This is another test message", "This is a final test message"])
    supervisor_sender: bool = Field(True, examples=[True, False])
    timestamp: datetime = Field(datetime.now(), examples=[datetime.now()])

class ChatMessage(BaseModel):
    agent_id: str = Field("text-green-500", examples=["text-green-500", "text-gray-500", "text-red-500"])
    messages: list[ChatMessageBody]
    