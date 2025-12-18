# Data Model: RAG Retrieval Function

## Overview
This document defines the data models for the RAG retrieval function that enables the chatbot to retrieve relevant book content and prevent hallucination.

## Core Entities

### Query
**Description:** Represents a user's question or request that needs to be answered using book content

**Fields:**
- `id`: string - Unique identifier for the query
- `text`: string - The actual text of the user's question
- `timestamp`: datetime - When the query was received
- `session_id`: string - Optional session identifier for conversation context
- `context`: QueryContext - Additional context for the query

### QueryContext
**Description:** Information about user's current context including selected text and conversation history

**Fields:**
- `selected_text`: string - Text selected by the user (if any) to limit search scope
- `conversation_history`: List[ChatMessage] - Previous messages in the conversation
- `user_preferences`: Dict[str, Any] - User-specific preferences for retrieval
- `filters`: Dict[str, Any] - Optional filters to apply to the search

### RetrievedContent
**Description:** Book content retrieved from Qdrant that matches the user's query with relevance score

**Fields:**
- `id`: string - Unique identifier for this retrieved content
- `chunk_id`: string - ID of the content chunk in storage
- `content`: string - The actual text content retrieved
- `source_file`: string - Name of the source file where content originated
- `source_location`: string - Specific location within the source (chapter, section, page, etc.)
- `relevance_score`: float - Similarity score between 0 and 1
- `embedding_vector`: List[float] - The vector representation of this content
- `metadata`: Dict[str, Any] - Additional metadata about the content
- `created_at`: datetime - When this content was originally embedded

### ChatMessage
**Description:** Individual message in a conversation, containing user input and AI response with source references

**Fields:**
- `id`: string - Unique identifier for the message
- `role`: string - 'user' or 'assistant'
- `content`: string - The text content of the message
- `timestamp`: datetime - When the message was created
- `source_references`: List[SourceReference] - References to source material used
- `query_id`: string - ID of the query that generated this response

### SourceReference
**Description:** Reference to the original source material used in a response

**Fields:**
- `source_file`: string - Name of the source file
- `source_location`: string - Location within the source file
- `content_snippet`: string - Snippet of the referenced content
- `confidence`: float - Confidence level in the relevance of this source
- `retrieved_content_id`: string - ID of the retrieved content that contains this reference

## Relationships
- A `Query` can result in multiple `RetrievedContent` items
- A `Query` exists within a `QueryContext`
- A `ChatMessage` can reference multiple `SourceReference` items
- A `SourceReference` points to specific content in a `RetrievedContent` item

## Validation Rules
- `Query.text` must not be empty or null
- `RetrievedContent.relevance_score` must be between 0 and 1
- `RetrievedContent.source_file` must be a valid book content file
- `SourceReference.confidence` must be between 0 and 1
- `ChatMessage.role` must be either 'user' or 'assistant'

## State Transitions (if applicable)
- `Query` starts in 'pending' state, transitions to 'processed' when retrieval is complete
- `RetrievedContent` is created in 'retrieved' state and may transition to 'validated' after quality checks