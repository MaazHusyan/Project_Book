"""
Pydantic models for Query and QueryContext entities
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from .chat_models import ChatMessage


class QueryContext(BaseModel):
    """
    Information about user's current context including selected text and conversation history
    """
    selected_text: Optional[str] = Field(
        default=None,
        description="Text selected by the user to limit search scope"
    )
    conversation_history: Optional[List[ChatMessage]] = Field(
        default_factory=list,
        description="Previous messages in the conversation"
    )
    user_preferences: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="User-specific preferences for retrieval"
    )
    filters: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Optional filters to apply to the search"
    )


class Query(BaseModel):
    """
    Represents a user's question or request that needs to be answered using book content
    """
    id: Optional[str] = Field(
        default=None,
        description="Unique identifier for the query"
    )
    text: str = Field(
        ...,
        description="The actual text of the user's question",
        min_length=1
    )
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="When the query was received"
    )
    session_id: Optional[str] = Field(
        default=None,
        description="Optional session identifier for conversation context"
    )
    context: QueryContext = Field(
        default_factory=QueryContext,
        description="Additional context for the query"
    )