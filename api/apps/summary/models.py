from pydantic import BaseModel

import logging
logger = logging.getLogger(__name__)

class Summary(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True