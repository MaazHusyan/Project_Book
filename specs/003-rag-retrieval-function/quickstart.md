# Quickstart: RAG Retrieval Function

## Overview
This guide provides a quick introduction to setting up and using the RAG retrieval function for the chatbot.

## Prerequisites
- Python 3.13
- Qdrant vector database running (either local or remote)
- Embedding API keys (Jina AI or Cohere)
- Book content already embedded in Qdrant

## Setup

### 1. Environment Configuration
```bash
# Copy the example environment file
cp backend/.env.example backend/.env

# Edit backend/.env with your configuration
QDRANT_URL=http://localhost:6333  # or your Qdrant URL
QDRANT_API_KEY=your_qdrant_api_key  # if using cloud
JINA_API_KEY=your_jina_api_key  # for Jina embeddings
COHERE_API_KEY=your_cohere_api_key  # for Cohere embeddings (optional)
EMBEDDING_MODEL=jina-embeddings-v3  # or embed-english-v3.0 for Cohere
```

### 2. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Verify Qdrant Connection
```bash
# Make sure Qdrant is running
curl http://localhost:6333/health
```

## Usage

### 1. Using the Retrieval API
```bash
# Example curl request to retrieve relevant content
curl -X POST http://localhost:8000/api/v1/retrieve \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the main principles of robot kinematics?",
    "top_k": 5,
    "filters": {
      "min_relevance_score": 0.5
    }
  }'
```

### 2. Expected Response
```json
{
  "query": "What are the main principles of robot kinematics?",
  "results": [
    {
      "id": "chunk-123",
      "content": "Robot kinematics is the study of motion in robotic systems...",
      "source_file": "03-kinematic-chains.mdx",
      "source_location": "Chapter 3, Section 1",
      "relevance_score": 0.87,
      "chunk_id": "kinematics-principles-001",
      "metadata": {}
    }
  ],
  "retrieved_at": "2025-12-18T10:30:00Z",
  "has_results": true
}
```

## Integration with Chatbot
The retrieval function is designed to be integrated with the chatbot agent to:
1. Retrieve relevant book content based on user queries
2. Provide source-attributed results to prevent hallucination
3. Return top-N most relevant results for response generation

## Testing
```bash
# Run unit tests
python -m pytest tests/embedding/test_embedding_storage.py

# Run integration tests
python -m pytest tests/embedding/test_integration.py
```

## Troubleshooting
- If retrieval returns no results, verify that book content is properly embedded in Qdrant
- If relevance scores are low, consider adjusting the min_relevance_score filter
- Check Qdrant connection and collection names match the configuration