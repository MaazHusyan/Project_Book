"""
Integration tests for the full retrieval workflow
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
import sys
import os

# Add backend/src to the Python path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from main import app
from src.retrieval.models.content_models import RetrievedContent


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.mark.asyncio
@patch('src.retrieval.services.retrieval_service.RetrievalService')
def test_retrieve_endpoint_success(mock_service_class, client):
    """Test successful content retrieval via the API endpoint"""
    # Mock the retrieval service
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

    # Make a request to the endpoint
    response = client.post(
        "/api/v1/retrieve",
        json={
            "query": "What is robotics?",
            "top_k": 5
        }
    )

    # Verify response
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "What is robotics?"
    assert data["has_results"] is True
    assert len(data["results"]) == 1
    assert data["results"][0]["content"] == "Test content for robotics"
    assert data["results"][0]["relevance_score"] == 0.85


@pytest.mark.asyncio
@patch('src.retrieval.services.retrieval_service.RetrievalService')
def test_retrieve_endpoint_short_query(mock_service_class, client):
    """Test retrieval with a query that's too short"""
    response = client.post(
        "/api/v1/retrieve",
        json={
            "query": "hi",  # Too short
            "top_k": 5
        }
    )

    # Should return 400 for short query
    assert response.status_code == 400


@pytest.mark.asyncio
@patch('src.retrieval.services.retrieval_service.RetrievalService')
def test_retrieve_endpoint_no_results(mock_service_class, client):
    """Test retrieval when no relevant content is found"""
    # Mock the retrieval service to return empty results
    mock_service_instance = AsyncMock()
    mock_service_class.return_value = mock_service_instance
    mock_service_instance.retrieve_content.return_value = []

    response = client.post(
        "/api/v1/retrieve",
        json={
            "query": "This is a test query with no matches",
            "top_k": 5
        }
    )

    # Should return 200 but with has_results=False
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "This is a test query with no matches"
    assert data["has_results"] is False
    assert len(data["results"]) == 0


@pytest.mark.asyncio
@patch('src.retrieval.services.retrieval_service.RetrievalService')
def test_retrieve_batch_endpoint_success(mock_service_class, client):
    """Test successful batch content retrieval"""
    # Mock the retrieval service
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

    # Make a request to the batch endpoint
    response = client.post(
        "/api/v1/retrieve/batch",
        json={
            "queries": [
                {
                    "query": "What is robotics?",
                    "top_k": 3
                },
                {
                    "query": "Explain kinematics",
                    "top_k": 3
                }
            ]
        }
    )

    # Verify response
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 2
    assert data["results"][0]["query"] == "What is robotics?"
    assert data["results"][1]["query"] == "Explain kinematics"
    assert data["results"][0]["has_results"] is True


@pytest.mark.asyncio
@patch('src.retrieval.services.retrieval_service.RetrievalService')
def test_retrieve_batch_endpoint_mixed_results(mock_service_class, client):
    """Test batch retrieval with mixed success/failure results"""
    # Mock the retrieval service to return different results for different calls
    mock_service_instance = AsyncMock()
    mock_service_class.return_value = mock_service_instance

    # First call returns results, second returns empty
    async def mock_retrieve_content(query, top_k=5):
        if query.text == "What is robotics?":
            return [
                RetrievedContent(
                    id="test1",
                    chunk_id="test1",
                    content="Test content for robotics",
                    source_file="robotics_book.pdf",
                    source_location="Chapter 1, Section 1",
                    relevance_score=0.85
                )
            ]
        else:
            return []  # No results for the second query

    mock_service_instance.retrieve_content.side_effect = mock_retrieve_content

    response = client.post(
        "/api/v1/retrieve/batch",
        json={
            "queries": [
                {
                    "query": "What is robotics?",
                    "top_k": 3
                },
                {
                    "query": "This has no matches",
                    "top_k": 3
                }
            ]
        }
    )

    # Verify response
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 2

    # First query should have results
    assert data["results"][0]["query"] == "What is robotics?"
    assert data["results"][0]["has_results"] is True
    assert len(data["results"][0]["results"]) == 1

    # Second query should have no results
    assert data["results"][1]["query"] == "This has no matches"
    assert data["results"][1]["has_results"] is False
    assert len(data["results"][1]["results"]) == 0


def test_root_endpoint(client):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "status" in data
    assert data["status"] == "healthy"


def test_health_endpoint(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "RAG Chatbot API"


@pytest.mark.asyncio
@patch('src.retrieval.services.retrieval_service.RetrievalService')
def test_retrieve_endpoint_with_context(mock_service_class, client):
    """Test retrieval with query context"""
    # Mock the retrieval service
    mock_service_instance = AsyncMock()
    mock_service_class.return_value = mock_service_instance

    mock_results = [
        RetrievedContent(
            id="test1",
            chunk_id="test1",
            content="Context-aware content",
            source_file="context_book.pdf",
            source_location="Section 2.3",
            relevance_score=0.90
        )
    ]
    mock_service_instance.retrieve_content.return_value = mock_results

    # Make a request with context
    response = client.post(
        "/api/v1/retrieve",
        json={
            "query": "Follow-up question",
            "top_k": 5,
            "context": {
                "selected_text": "Previous discussion about robotics",
                "filters": {
                    "source_file": "robotics_book.pdf"
                }
            }
        }
    )

    # Verify response
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "Follow-up question"
    assert data["has_results"] is True
    assert len(data["results"]) == 1
    assert data["results"][0]["content"] == "Context-aware content"