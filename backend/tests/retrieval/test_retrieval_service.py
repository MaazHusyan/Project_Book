"""
Unit tests for retrieval service functionality
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.retrieval.services.retrieval_service import RetrievalService
from src.retrieval.models.query_models import Query, QueryContext
from src.retrieval.models.content_models import RetrievedContent


@pytest.fixture
def mock_qdrant_retriever():
    """Mock QdrantRetriever for testing"""
    mock = AsyncMock()
    mock.search = AsyncMock()
    return mock


@pytest.fixture
def retrieval_service(mock_qdrant_retriever):
    """Create a retrieval service instance with mocked dependencies"""
    # Since the import happens inside __init__, we need to patch it at the module level
    # where the service will import it from
    with patch('src.retrieval.utils.qdrant_retriever.QdrantRetriever', return_value=mock_qdrant_retriever):
        service = RetrievalService()
        yield service


@pytest.mark.asyncio
async def test_retrieve_content_success(retrieval_service, mock_qdrant_retriever):
    """Test successful content retrieval"""
    # Arrange
    query = Query(text="What is robot kinematics?")
    mock_content = [
        RetrievedContent(
            id="test1",
            chunk_id="test1",
            content="Robot kinematics is the study of motion in robotic systems",
            source_file="robotics_book.pdf",
            source_location="Chapter 3, Section 1",
            relevance_score=0.85
        )
    ]
    mock_qdrant_retriever.search.return_value = mock_content

    # Act
    result = await retrieval_service.retrieve_content(query)

    # Assert
    assert len(result) == 1
    assert result[0].content == "Robot kinematics is the study of motion in robotic systems"
    assert result[0].relevance_score == 0.85
    mock_qdrant_retriever.search.assert_called_once()


@pytest.mark.asyncio
async def test_retrieve_content_empty_query():
    """Test retrieval with minimal query (empty after validation) raises exception"""
    service = RetrievalService()

    # Use a query that will fail validation (too short)
    query = Query(text="a")

    with pytest.raises(ValueError):
        await service.retrieve_content(query)


@pytest.mark.asyncio
async def test_retrieve_content_minimal_query():
    """Test retrieval with minimal query (less than 3 chars)"""
    service = RetrievalService()

    query = Query(text="hi")

    with pytest.raises(ValueError):
        await service.retrieve_content(query)


@pytest.mark.asyncio
async def test_validate_query_valid():
    """Test query validation with valid query"""
    service = RetrievalService()
    query = Query(text="What is artificial intelligence?")

    result = await service.validate_query(query)
    assert result is True


@pytest.mark.asyncio
async def test_validate_query_empty():
    """Test query validation with empty query"""
    service = RetrievalService()
    query = Query(text="a")  # Use a short query that will fail validation

    result = await service.validate_query(query)
    assert result is False


@pytest.mark.asyncio
async def test_validate_query_too_short():
    """Test query validation with too short query"""
    service = RetrievalService()
    query = Query(text="hi")

    result = await service.validate_query(query)
    assert result is False


@pytest.mark.asyncio
async def test_validate_query_suspicious_content():
    """Test query validation with suspicious content"""
    service = RetrievalService()
    query = Query(text="What is <script>alert('test')</script>?")

    result = await service.validate_query(query)
    assert result is False


@pytest.mark.asyncio
async def test_retrieve_content_batch():
    """Test batch content retrieval"""
    service = RetrievalService()
    service.qdrant_retriever = AsyncMock()
    service.qdrant_retriever.search = AsyncMock(return_value=[
        RetrievedContent(
            id="test1",
            chunk_id="test1",
            content="Test content",
            source_file="test.pdf",
            source_location="Section 1",
            relevance_score=0.75
        )
    ])

    queries = [
        Query(text="First query"),
        Query(text="Second query")
    ]

    results = await service.retrieve_content_batch(queries)

    assert len(results) == 2
    assert len(results[0]) == 1
    assert len(results[1]) == 1
    assert results[0][0].content == "Test content"