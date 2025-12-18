"""
Integration tests for RAG integration service
"""
import pytest
from unittest.mock import AsyncMock, patch
from src.retrieval.services.rag_integration_service import RAGIntegrationService
from src.retrieval.models.content_models import RetrievedContent


@pytest.mark.asyncio
async def test_get_relevant_content_for_query():
    """Test getting relevant content for a query"""
    # Mock the retrieval service
    with patch('src.retrieval.services.rag_integration_service.RetrievalService') as mock_service_class:
        mock_service_instance = AsyncMock()
        mock_service_class.return_value = mock_service_instance

        mock_results = [
            RetrievedContent(
                id="test1",
                chunk_id="test1",
                content="Test content for robotics",
                source_file="robotics_book.pdf",
                source_location="Chapter 1, Section 1",
                relevance_score=0.85
            )
        ]
        mock_service_instance.retrieve_content.return_value = mock_results

        # Create RAG integration service
        rag_service = RAGIntegrationService()

        # Test the method
        results = await rag_service.get_relevant_content_for_query(
            query_text="What is robotics?",
            top_k=5
        )

        # Verify results
        assert len(results) == 1
        assert results[0].content == "Test content for robotics"
        assert results[0].relevance_score == 0.85
        mock_service_instance.retrieve_content.assert_called_once()


@pytest.mark.asyncio
async def test_get_relevant_content_with_context():
    """Test getting relevant content with conversation context"""
    with patch('src.retrieval.services.rag_integration_service.RetrievalService') as mock_service_class:
        mock_service_instance = AsyncMock()
        mock_service_class.return_value = mock_service_instance

        mock_results = [
            RetrievedContent(
                id="test2",
                chunk_id="test2",
                content="Context-aware content",
                source_file="context_book.pdf",
                source_location="Section 2.3",
                relevance_score=0.90
            )
        ]
        mock_service_instance.retrieve_content.return_value = mock_results

        # Create conversation context
        conversation_context = [
            {
                "role": "user",
                "content": "Previous question about robotics",
                "timestamp": "2023-01-01T00:00:00Z"
            },
            {
                "role": "assistant",
                "content": "Previous answer about robotics",
                "timestamp": "2023-01-01T00:00:01Z"
            }
        ]

        # Create RAG integration service
        rag_service = RAGIntegrationService()

        # Test the method
        results = await rag_service.get_relevant_content_with_context(
            query_text="Follow-up about kinematics",
            conversation_context=conversation_context,
            top_k=3
        )

        # Verify results
        assert len(results) == 1
        assert results[0].content == "Context-aware content"
        mock_service_instance.retrieve_content.assert_called_once()


@pytest.mark.asyncio
async def test_validate_content_relevance():
    """Test content relevance validation"""
    rag_service = RAGIntegrationService()

    # Create test content
    test_content = [
        RetrievedContent(
            id="test1",
            chunk_id="test1",
            content="High relevance content",
            source_file="test.pdf",
            source_location="Section 1",
            relevance_score=0.85
        ),
        RetrievedContent(
            id="test2",
            chunk_id="test2",
            content="Low relevance content",
            source_file="test.pdf",
            source_location="Section 2",
            relevance_score=0.30
        )
    ]

    # Test with high relevance threshold
    is_relevant = await rag_service.validate_content_relevance(
        query_text="test query",
        retrieved_content=test_content,
        min_relevance_score=0.5
    )
    assert is_relevant is True

    # Test with low relevance threshold
    is_relevant = await rag_service.validate_content_relevance(
        query_text="test query",
        retrieved_content=test_content,
        min_relevance_score=0.9
    )
    assert is_relevant is False

    # Test with no content
    is_relevant = await rag_service.validate_content_relevance(
        query_text="test query",
        retrieved_content=[],
        min_relevance_score=0.5
    )
    assert is_relevant is False


@pytest.mark.asyncio
async def test_empty_content_list():
    """Test behavior with empty content list"""
    rag_service = RAGIntegrationService()

    is_relevant = await rag_service.validate_content_relevance(
        query_text="test query",
        retrieved_content=[],
        min_relevance_score=0.5
    )
    assert is_relevant is False