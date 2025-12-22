# RAG Chatbot Retrieval API Documentation

## Overview

The RAG Chatbot Retrieval API provides semantic search capabilities over robotics book content. The API enables users to query the knowledge base and retrieve relevant passages with source attribution.

## Base URL

All endpoints are available under the `/api/v1` prefix.

## Authentication

This API does not require authentication for basic functionality, but rate limiting is enforced.

## Rate Limiting

- Single requests: Limited by the rate limiter configuration
- Batch requests: Maximum batch size is limited by `BATCH_SIZE_LIMIT` configuration
- Default rate limit: 10 requests per minute per IP

## Endpoints

### POST /api/v1/retrieve

Retrieve relevant book content for a single user query.

#### Request

**Content-Type**: `application/json`

**Body**:
```json
{
  "query": "string (required)",
  "top_k": "integer (optional, default: 5)",
  "filters": "object (optional)",
  "context": "QueryContext object (optional)"
}
```

**Fields**:
- `query`: The user's query text (minimum 3 characters)
- `top_k`: Number of top results to return (default: 5, max: configured limit)
- `filters`: Additional filters to apply to the search
  - `source_file`: Filter by specific source file
  - Additional filters may be supported
- `context`: Query context for enhanced retrieval
  - `conversation_history`: List of previous conversation turns
  - `selected_text`: Text that should be the focus of the query
  - `filters`: Context-specific filters

#### Response

**Status Code**: `200 OK`

**Content-Type**: `application/json`

```json
{
  "query": "string",
  "results": [
    {
      "id": "string",
      "chunk_id": "string",
      "content": "string",
      "source_file": "string",
      "source_location": "string",
      "relevance_score": "float"
    }
  ],
  "retrieved_at": "datetime (ISO 8601)",
  "has_results": "boolean"
}
```

#### Error Responses

- `400 Bad Request`: Query is too short (< 3 characters) or invalid
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error during retrieval

#### Example Request

```json
{
  "query": "What is robot kinematics?",
  "top_k": 3,
  "filters": {
    "source_file": "robotics_book_chapter_3.pdf"
  },
  "context": {
    "conversation_history": [
      {
        "role": "user",
        "content": "I'm learning about robotics"
      },
      {
        "role": "assistant",
        "content": "Great! Robotics involves several key areas including kinematics, dynamics, and control."
      }
    ]
  }
}
```

#### Example Response

```json
{
  "query": "What is robot kinematics?",
  "results": [
    {
      "id": "doc123",
      "chunk_id": "chunk456",
      "content": "Robot kinematics is the study of motion in robotic systems, focusing on the relationship between joint variables and the position and orientation of the robot's end-effector.",
      "source_file": "robotics_book_chapter_3.pdf",
      "source_location": "Chapter 3, Section 2.1",
      "relevance_score": 0.87
    }
  ],
  "retrieved_at": "2025-12-18T10:30:00.123456",
  "has_results": true
}
```

### POST /api/v1/retrieve/batch

Retrieve relevant content for multiple queries in a single batch request.

#### Request

**Content-Type**: `application/json`

**Body**:
```json
{
  "queries": [
    {
      "query": "string (required)",
      "top_k": "integer (optional)",
      "filters": "object (optional)",
      "context": "QueryContext object (optional)"
    }
  ],
  "top_k": "integer (optional, default: 5)"
}
```

#### Response

**Status Code**: `200 OK`

**Content-Type**: `application/json`

```json
{
  "results": [
    {
      "query": "string",
      "results": [
        {
          "id": "string",
          "chunk_id": "string",
          "content": "string",
          "source_file": "string",
          "source_location": "string",
          "relevance_score": "float"
        }
      ],
      "retrieved_at": "datetime (ISO 8601)",
      "has_results": "boolean"
    }
  ]
}
```

#### Error Responses

- `400 Bad Request`: Batch size exceeds limit or invalid query in batch
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error during batch retrieval

## Performance Characteristics

- **Response Time**: Single queries typically complete in <2 seconds
- **Caching**: Results are cached for 10 minutes to improve performance for repeated queries
- **Batch Processing**: Individual queries in a batch are processed independently
- **Rate Limiting**: API is rate-limited to prevent abuse

## Query Validation

All queries undergo validation:

- Minimum length: 3 characters
- Security filtering: Prevents XSS attempts with patterns like `<script`, `javascript:`, etc.
- Context enhancement: Queries can be enhanced with conversation history and filters

## Error Handling

The API provides detailed error messages:

- `QueryProcessingError`: Issues with query format or content
- `NoRelevantContentError`: No content found for the query (returns empty results with success status)
- `RetrievalError`: Issues with the retrieval process
- General exceptions: Internal server errors

## Content Quality

- **Relevance Scoring**: Results include relevance scores between 0 and 1
- **Source Attribution**: Each result includes source file and location
- **Context Awareness**: Query enhancement with conversation history improves relevance
- **Filtering**: Results are filtered by minimum relevance threshold

## Integration with RAG System

The retrieval API is designed to work seamlessly with RAG (Retrieval-Augmented Generation) systems:

1. Query the `/retrieve` endpoint with user input
2. Use the returned content as context for the language model
3. Generate responses that reference the provided sources
4. Ensure response grounding in retrieved content

## Health Check Endpoints

The main application also provides health check endpoints:

- `GET /`: Root endpoint with health status
- `GET /health`: Dedicated health check