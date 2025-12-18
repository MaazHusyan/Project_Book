"""
Integration tests for Qdrant retrieval functionality
"""
import pytest
from unittest.mock import patch, AsyncMock
from src.retrieval.utils.qdrant_retriever import QdrantRetriever
from src.retrieval.models.content_models import RetrievedContent


@pytest.mark.asyncio
async def test_qdrant_retriever_search():
    """Test Qdrant retriever search functionality"""
    # Mock the Qdrant client and embedding service
    with patch('src.retrieval.utils.qdrant_retriever.QdrantClient') as mock_qdrant_client, \
         patch('src.retrieval.utils.qdrant_retriever.EmbeddingServiceFactory') as mock_factory:

        # Setup mock client
        mock_client_instance = AsyncMock()
        mock_qdrant_client.return_value = mock_client_instance

        # Setup mock embedding service
        mock_embedding_service = AsyncMock()
        mock_factory.create_embedding_service.return_value = mock_embedding_service
        mock_embedding_service.embed_text.return_value = [0.1, 0.2, 0.3, 0.4]  # Mock embedding

        # Setup mock search results
        mock_search_result = [
            type('obj', (object,), {
                'id': 'test_id_1',
                'payload': {
                    'content': 'Test content for robotics',
                    'source_file': 'robotics_book.pdf',
                    'source_location': 'Chapter 1, Section 1',
                    'metadata': {}
                },
                'score': 0.85
            })()
        ]
        mock_client_instance.search.return_value = mock_search_result

        # Create QdrantRetriever instance
        retriever = QdrantRetriever()

        # Perform search
        results = await retriever.search("robotics concepts", top_k=5)

        # Verify results
        assert len(results) == 1
        assert isinstance(results[0], RetrievedContent)
        assert results[0].content == 'Test content for robotics'
        assert results[0].source_file == 'robotics_book.pdf'
        assert results[0].relevance_score == 0.85


@pytest.mark.asyncio
async def test_qdrant_retriever_with_filters():
    """Test Qdrant retriever with filters"""
    with patch('src.retrieval.utils.qdrant_retriever.QdrantClient') as mock_qdrant_client, \
         patch('src.retrieval.utils.qdrant_retriever.EmbeddingServiceFactory') as mock_factory:

        # Setup mock client
        mock_client_instance = AsyncMock()
        mock_qdrant_client.return_value = mock_client_instance

        # Setup mock embedding service
        mock_embedding_service = AsyncMock()
        mock_factory.create_embedding_service.return_value = mock_embedding_service
        mock_embedding_service.embed_text.return_value = [0.1, 0.2, 0.3, 0.4]

        # Setup mock search results
        mock_search_result = [
            type('obj', (object,), {
                'id': 'test_id_1',
                'payload': {
                    'content': 'Filtered test content',
                    'source_file': 'specific_chapter.pdf',
                    'source_location': 'Section 2.1',
                    'metadata': {}
                },
                'score': 0.90
            })()
        ]
        mock_client_instance.search.return_value = mock_search_result

        # Create QdrantRetriever instance
        retriever = QdrantRetriever()

        # Perform search with filters
        filters = {"source_file": "specific_chapter.pdf"}
        results = await retriever.search("specific topic", top_k=5, filters=filters)

        # Verify results
        assert len(results) == 1
        assert results[0].content == 'Filtered test content'
        assert results[0].source_file == 'specific_chapter.pdf'


@pytest.mark.asyncio
async def test_qdrant_retriever_empty_results():
    """Test Qdrant retriever with no results"""
    with patch('src.retrieval.utils.qdrant_retriever.QdrantClient') as mock_qdrant_client, \
         patch('src.retrieval.utils.qdrant_retriever.EmbeddingServiceFactory') as mock_factory:

        # Setup mock client
        mock_client_instance = AsyncMock()
        mock_qdrant_client.return_value = mock_client_instance

        # Setup mock embedding service
        mock_embedding_service = AsyncMock()
        mock_factory.create_embedding_service.return_value = mock_embedding_service
        mock_embedding_service.embed_text.return_value = [0.1, 0.2, 0.3, 0.4]

        # Setup empty search results
        mock_client_instance.search.return_value = []

        # Create QdrantRetriever instance
        retriever = QdrantRetriever()

        # Perform search
        results = await retriever.search("unrelated query", top_k=5)

        # Verify empty results
        assert len(results) == 0


def test_build_filter():
    """Test the _build_filter method"""
    retriever = QdrantRetriever()

    # Test with no filters
    result = retriever._build_filter(None)
    assert result is None

    # Test with source_file filter
    filters = {"source_file": "test.pdf"}
    result = retriever._build_filter(filters)
    assert result is not None