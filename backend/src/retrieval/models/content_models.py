"""
Pydantic models for RetrievedContent and SourceReference entities
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class SourceReference(BaseModel):
    """
    Reference to the original source material used in a response
    """
    source_file: str = Field(
        ...,
        description="Name of the source file"
    )
    source_location: str = Field(
        ...,
        description="Location within the source file"
    )
    content_snippet: str = Field(
        ...,
        description="Snippet of the referenced content"
    )
    confidence: float = Field(
        ...,
        description="Confidence level in the relevance of this source",
        ge=0.0,
        le=1.0
    )
    retrieved_content_id: Optional[str] = Field(
        default=None,
        description="ID of the retrieved content that contains this reference"
    )


class RetrievedContent(BaseModel):
    """
    Book content retrieved from Qdrant that matches the user's query with relevance score
    """
    id: str = Field(
        ...,
        description="Unique identifier for this retrieved content"
    )
    chunk_id: str = Field(
        ...,
        description="ID of the content chunk in storage"
    )
    content: str = Field(
        ...,
        description="The actual text content retrieved"
    )
    source_file: str = Field(
        ...,
        description="Name of the source file where content originated"
    )
    source_location: str = Field(
        ...,
        description="Specific location within the source (chapter, section, page, etc.)"
    )
    relevance_score: float = Field(
        ...,
        description="Similarity score between 0 and 1",
        ge=0.0,
        le=1.0
    )
    embedding_vector: Optional[List[float]] = Field(
        default=None,
        description="The vector representation of this content"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional metadata about the content"
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="When this content was originally embedded"
    )