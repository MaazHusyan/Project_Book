"""
Configuration for the RAG retrieval function
"""
import os
from typing import Optional


class RetrievalConfig:
    """Configuration class for retrieval functionality"""

    # Qdrant configuration
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY: Optional[str] = os.getenv("QDRANT_API_KEY")
    QDRANT_COLLECTION_NAME: str = os.getenv("QDRANT_COLLECTION_NAME", "robotics_book_embeddings")

    # Retrieval parameters
    DEFAULT_TOP_K: int = int(os.getenv("DEFAULT_TOP_K", "5"))
    MAX_TOP_K: int = int(os.getenv("MAX_TOP_K", "10"))
    MIN_RELEVANCE_SCORE: float = float(os.getenv("MIN_RELEVANCE_SCORE", "0.5"))

    # Performance settings
    RETRIEVAL_TIMEOUT: int = int(os.getenv("RETRIEVAL_TIMEOUT", "30"))  # seconds
    BATCH_SIZE_LIMIT: int = int(os.getenv("BATCH_SIZE_LIMIT", "10"))

    # Embedding model configuration
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "jina-embeddings-v3")