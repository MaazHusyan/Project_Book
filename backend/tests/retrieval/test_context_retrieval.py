"""
Tests for context-aware retrieval functionality
"""
import pytest
from unittest.mock import AsyncMock
from src.retrieval.services.retrieval_service import RetrievalService
from src.retrieval.models.query_models import Query, QueryContext
from src.retrieval.models.chat_models import ChatMessage
from src.retrieval.models.content_models import RetrievedContent


@pytest.mark.asyncio
async def test_enhance_query_with_conversation_context():
    """Test query enhancement with conversation history"""
    service = RetrievalService()

    # Create conversation history
    conversation_history = [
        ChatMessage(role="user", content="What is robot kinematics?"),
        ChatMessage(role="assistant", content="Robot kinematics is the study of motion in robotic systems"),
        ChatMessage(role="user", content="Can you explain forward kinematics?")
    ]

    query_context = QueryContext(conversation_history=conversation_history)
    query = Query(text="detailed explanation", context=query_context)

    enhanced_query = await service._enhance_query_with_context(query)

    # Check that the context was incorporated
    assert "Context:" in enhanced_query
    assert "forward kinematics" in enhanced_query
    assert "Current Query: detailed explanation" in enhanced_query


@pytest.mark.asyncio
async def test_enhance_query_with_selected_text():
    """Test query enhancement with selected text"""
    service = RetrievalService()

    query_context = QueryContext(selected_text="Chapter 3 discusses robot actuators")
    query = Query(text="How do they work?", context=query_context)

    enhanced_query = await service._enhance_query_with_context(query)

    # Check that the selected text was incorporated
    assert "Focus on: Chapter 3 discusses robot actuators" in enhanced_query
    assert "Query: How do they work?" in enhanced_query


@pytest.mark.asyncio
async def test_enhance_query_with_source_filter():
    """Test query enhancement with source file filter"""
    service = RetrievalService()

    filters = {"source_file": "robotics_fundamentals.pdf"}
    query_context = QueryContext(filters=filters)
    query = Query(text="What are the main principles?", context=query_context)

    enhanced_query = await service._enhance_query_with_context(query)

    # Check that the source file was incorporated
    assert "From robotics_fundamentals.pdf: What are the main principles?" in enhanced_query


@pytest.mark.asyncio
async def test_enhance_query_no_context():
    """Test query enhancement with no context (should return original)"""
    service = RetrievalService()

    query = Query(text="What is artificial intelligence?")

    enhanced_query = await service._enhance_query_with_context(query)

    # Should return the original query unchanged
    assert enhanced_query == "What is artificial intelligence?"


@pytest.mark.asyncio
async def test_retrieve_content_with_context():
    """Test retrieval with context enhancement"""
    service = RetrievalService()
    service.qdrant_retriever = AsyncMock()
    service.qdrant_retriever.search = AsyncMock(return_value=[
        RetrievedContent(
            id="test1",
            chunk_id="test1",
            content="Contextually relevant content",
            source_file="robotics_book.pdf",
            source_location="Chapter 3, Section 2",
            relevance_score=0.88
        )
    ])

    # Create a query with conversation context
    conversation_history = [
        ChatMessage(role="user", content="Explain robot sensors"),
        ChatMessage(role="assistant", content="Sensors help robots perceive their environment")
    ]
    query_context = QueryContext(conversation_history=conversation_history)
    query = Query(text="What types exist?", context=query_context)

    results = await service.retrieve_content(query)

    # Verify that the search was called with an enhanced query
    assert len(results) == 1
    assert results[0].content == "Contextually relevant content"
    # The search method should have been called with the enhanced query text
    service.qdrant_retriever.search.assert_called_once()


@pytest.mark.asyncio
async def test_session_context_methods():
    """Test session context management methods"""
    service = RetrievalService()

    # Test getting session context
    context = await service.get_session_context("test_session_123")
    assert context is not None
    assert hasattr(context, 'conversation_history')

    # Test saving session context
    new_context = QueryContext()
    await service.save_session_context("test_session_123", new_context)
    # This should not raise an exception (placeholder implementation)