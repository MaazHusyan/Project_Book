"""
Pydantic models for ChatMessage entity
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from .content_models import SourceReference


class ChatMessage(BaseModel):
    """
    Individual message in a conversation, containing user input and AI response with source references
    """
    id: Optional[str] = Field(
        default=None,
        description="Unique identifier for the message"
    )
    role: str = Field(
        ...,
        description="Role of the message sender",
        pattern=r"^(user|assistant)$"
    )
    content: str = Field(
        ...,
        description="The text content of the message"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="When the message was created"
    )
    source_references: Optional[List[SourceReference]] = Field(
        default_factory=list,
        description="References to source material used"
    )
    query_id: Optional[str] = Field(
        default=None,
        description="ID of the query that generated this response"
    )

    @validator('role')
    def validate_role(cls, v):
        if v not in ['user', 'assistant']:
            raise ValueError('Role must be either "user" or "assistant"')
        return v