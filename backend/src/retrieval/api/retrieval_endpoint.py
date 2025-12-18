"""
API endpoints for retrieval functionality based on contracts
"""
import time
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import logging
import traceback

from ..models.query_models import Query as RetrievalQuery, QueryContext
from ..models.content_models import RetrievedContent
from ..services.retrieval_service import RetrievalService
from ..services.rag_integration_service import RAGIntegrationService
from ...utils.rate_limiter import RateLimiter  # Using existing rate limiter from main utils
from ..config import RetrievalConfig
from ..exceptions import RetrievalError, NoRelevantContentError, QueryProcessingError


# Request/Response models that match the API contract
class RetrievalRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    filters: Optional[dict] = {}
    context: Optional[QueryContext] = None


class RetrievalResponse(BaseModel):
    query: str
    results: List[RetrievedContent]
    retrieved_at: datetime
    has_results: bool


class BatchRetrievalRequest(BaseModel):
    queries: List[RetrievalRequest]
    top_k: Optional[int] = 5


class BatchRetrievalResponse(BaseModel):
    results: List[RetrievalResponse]


class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[dict] = None


# Create router
router = APIRouter(prefix="/api/v1", tags=["retrieval"])

# Initialize services
retrieval_service = RetrievalService()
rag_service = RAGIntegrationService()
config = RetrievalConfig()
rate_limiter = RateLimiter(max_requests=config.BATCH_SIZE_LIMIT, time_window_seconds=60)
logger = logging.getLogger(__name__)


@router.post("/retrieve", response_model=RetrievalResponse)
async def retrieve_content(
    request: RetrievalRequest,
    background_tasks: BackgroundTasks
):
    """
    Retrieve relevant book content for a user query

    This endpoint performs semantic search against the robotics book content
    to find the most relevant passages for the user's query. The search is
    enhanced with context awareness and relevance filtering to provide
    high-quality results.

    Args:
        request (RetrievalRequest): The retrieval request containing:
            - query (str): The user's query text (min 3 characters)
            - top_k (int, optional): Number of results to return (default: 5)
            - filters (dict, optional): Additional filters to apply
            - context (QueryContext, optional): Query context for enhanced retrieval
        background_tasks (BackgroundTasks): FastAPI background tasks for async operations

    Returns:
        RetrievalResponse: Response containing:
            - query (str): The original query text
            - results (List[RetrievedContent]): List of retrieved content items
            - retrieved_at (datetime): Timestamp of retrieval
            - has_results (bool): Whether any results were found

    Raises:
        HTTPException: With appropriate status codes for various error conditions:
            - 400: Invalid query (too short, processing error)
            - 429: Rate limit exceeded
            - 500: Internal server error during retrieval

    Example:
        Request:
        {
            "query": "What is robot kinematics?",
            "top_k": 3,
            "filters": {"source_file": "robotics_book_chapter_3.pdf"}
        }

        Response:
        {
            "query": "What is robot kinematics?",
            "results": [
                {
                    "id": "doc123",
                    "chunk_id": "chunk456",
                    "content": "Robot kinematics is the study of motion in robotic systems...",
                    "source_file": "robotics_book_chapter_3.pdf",
                    "source_location": "Chapter 3, Section 2.1",
                    "relevance_score": 0.87
                }
            ],
            "retrieved_at": "2025-12-18T10:30:00.123456",
            "has_results": true
        }
    """
    start_time = time.time()
    logger.info(f"API request received for single retrieval | Query: {request.query[:50]}...")

    try:
        # Rate limiting
        if not rate_limiter.can_acquire():
            rate_limit_time = time.time() - start_time
            logger.warning(f"Rate limit exceeded | Request time: {rate_limit_time:.3f}s | Query: {request.query[:50]}...")
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded"
            )

        # Validate the query length
        if len(request.query.strip()) < 3:
            validation_time = time.time() - start_time
            logger.warning(f"Query validation failed - too short | Request time: {validation_time:.3f}s | Query: {request.query[:50]}...")
            raise HTTPException(
                status_code=400,
                detail="Query must be at least 3 characters long"
            )

        # Create a Query object from the request
        query_obj = RetrievalQuery(
            text=request.query,
            context=request.context or QueryContext()
        )

        # Retrieve content using the service
        results = await retrieval_service.retrieve_content(
            query=query_obj,
            top_k=request.top_k
        )

        # Create response
        response = RetrievalResponse(
            query=request.query,
            results=results,
            retrieved_at=datetime.now(),
            has_results=len(results) > 0
        )

        total_time = time.time() - start_time
        logger.info(f"API request completed successfully | Total time: {total_time:.3f}s | Results: {len(results)} | Query: {request.query[:50]}...")

        return response

    except HTTPException:
        # Re-raise HTTP exceptions
        total_time = time.time() - start_time
        logger.warning(f"HTTP exception in API request | Total time: {total_time:.3f}s | Query: {request.query[:50]}...")
        raise
    except QueryProcessingError as e:
        total_time = time.time() - start_time
        logger.error(f"Query processing error in API request | Total time: {total_time:.3f}s | Error: {str(e)} | Query: {request.query[:50]}...")
        raise HTTPException(
            status_code=400,
            detail=f"Query processing error: {str(e)}"
        )
    except NoRelevantContentError as e:
        total_time = time.time() - start_time
        logger.warning(f"No relevant content found in API request | Total time: {total_time:.3f}s | Query: {request.query[:50]}... - {str(e)}")
        # Return empty results but with success status
        response = RetrievalResponse(
            query=request.query,
            results=[],
            retrieved_at=datetime.now(),
            has_results=False
        )
        return response
    except RetrievalError as e:
        total_time = time.time() - start_time
        logger.error(f"Retrieval error in API request | Total time: {total_time:.3f}s | Error: {str(e)} | Query: {request.query[:50]}...")
        raise HTTPException(
            status_code=500,
            detail=f"Retrieval error: {str(e)}"
        )
    except Exception as e:
        total_time = time.time() - start_time
        logger.error(f"Unexpected error in API request: {str(e)} | Total time: {total_time:.3f}s | Query: {request.query[:50]}...\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during content retrieval"
        )


@router.post("/retrieve/batch", response_model=BatchRetrievalResponse)
async def retrieve_content_batch(
    request: BatchRetrievalRequest,
    background_tasks: BackgroundTasks
):
    """
    Retrieve relevant content for multiple queries in a single batch request

    This endpoint allows efficient retrieval of content for multiple queries
    in one API call. Each query is processed individually with the same
    semantic search and context enhancement as the single retrieval endpoint.

    Args:
        request (BatchRetrievalRequest): The batch retrieval request containing:
            - queries (List[RetrievalRequest]): List of individual retrieval requests
            - top_k (int, optional): Default number of results per query (default: 5)
        background_tasks (BackgroundTasks): FastAPI background tasks for async operations

    Returns:
        BatchRetrievalResponse: Response containing:
            - results (List[RetrievalResponse]): List of individual retrieval responses

    Raises:
        HTTPException: With appropriate status codes for various error conditions:
            - 400: Batch size exceeds limit or invalid query in batch
            - 429: Rate limit exceeded
            - 500: Internal server error during batch retrieval

    Example:
        Request:
        [
            {
                "query": "What is robot kinematics?",
                "top_k": 3
            },
            {
                "query": "Explain inverse kinematics",
                "top_k": 2,
                "filters": {"source_file": "robotics_book_chapter_3.pdf"}
            }
        ]

        Response:
        {
            "results": [
                {
                    "query": "What is robot kinematics?",
                    "results": [...],
                    "retrieved_at": "2025-12-18T10:30:00.123456",
                    "has_results": true
                },
                {
                    "query": "Explain inverse kinematics",
                    "results": [...],
                    "retrieved_at": "2025-12-18T10:30:00.123457",
                    "has_results": true
                }
            ]
        }

    Performance Notes:
        - Maximum batch size is limited by config.BATCH_SIZE_LIMIT
        - Each query in the batch is processed independently
        - Individual query failures do not affect other queries in the batch
        - Response maintains the same order as the input queries
    """
    start_time = time.time()
    logger.info(f"API request received for batch retrieval | Batch size: {len(request.queries)}")

    try:
        # Rate limiting - limit batch size
        if len(request.queries) > config.BATCH_SIZE_LIMIT:
            batch_validation_time = time.time() - start_time
            logger.warning(f"Batch size exceeds limit | Request time: {batch_validation_time:.3f}s | Size: {len(request.queries)} | Limit: {config.BATCH_SIZE_LIMIT}")
            raise HTTPException(
                status_code=400,
                detail=f"Batch size exceeds maximum limit of {config.BATCH_SIZE_LIMIT}"
            )

        # Process each query in the batch
        results = []
        successful_queries = 0
        failed_queries = 0

        for i, single_request in enumerate(request.queries):
            query_start_time = time.time()
            try:
                # Validate the query length
                if len(single_request.query.strip()) < 3:
                    # Add error response for this query
                    error_response = RetrievalResponse(
                        query=single_request.query,
                        results=[],
                        retrieved_at=datetime.now(),
                        has_results=False
                    )
                    results.append(error_response)
                    failed_queries += 1
                    logger.debug(f"Batch query {i+1} validation failed - too short | Query: {single_request.query[:30]}...")
                    continue

                # Create a Query object from the request
                query_obj = RetrievalQuery(
                    text=single_request.query,
                    context=single_request.context or QueryContext()
                )

                # Retrieve content for this query
                query_results = await retrieval_service.retrieve_content(
                    query=query_obj,
                    top_k=single_request.top_k or request.top_k
                )

                # Create response for this query
                query_response = RetrievalResponse(
                    query=single_request.query,
                    results=query_results,
                    retrieved_at=datetime.now(),
                    has_results=len(query_results) > 0
                )

                results.append(query_response)
                successful_queries += 1
                query_time = time.time() - query_start_time
                logger.debug(f"Batch query {i+1} completed successfully | Time: {query_time:.3f}s | Results: {len(query_results)} | Query: {single_request.query[:30]}...")

            except QueryProcessingError as e:
                query_time = time.time() - query_start_time
                logger.error(f"Query processing error for batch query {i+1} | Time: {query_time:.3f}s | Error: {str(e)} | Query: {single_request.query[:30]}...")
                error_response = RetrievalResponse(
                    query=single_request.query,
                    results=[],
                    retrieved_at=datetime.now(),
                    has_results=False
                )
                results.append(error_response)
                failed_queries += 1

            except NoRelevantContentError as e:
                query_time = time.time() - query_start_time
                logger.warning(f"No relevant content for batch query {i+1} | Time: {query_time:.3f}s | Query: {single_request.query[:30]}... - {str(e)}")
                error_response = RetrievalResponse(
                    query=single_request.query,
                    results=[],
                    retrieved_at=datetime.now(),
                    has_results=False
                )
                results.append(error_response)
                failed_queries += 1

            except RetrievalError as e:
                query_time = time.time() - query_start_time
                logger.error(f"Retrieval error for batch query {i+1} | Time: {query_time:.3f}s | Error: {str(e)} | Query: {single_request.query[:30]}...")
                error_response = RetrievalResponse(
                    query=single_request.query,
                    results=[],
                    retrieved_at=datetime.now(),
                    has_results=False
                )
                results.append(error_response)
                failed_queries += 1

            except Exception as e:
                query_time = time.time() - query_start_time
                logger.error(f"Unexpected error for batch query {i+1} | Time: {query_time:.3f}s | Error: {str(e)} | Query: {single_request.query[:30]}...\n{traceback.format_exc()}")
                error_response = RetrievalResponse(
                    query=single_request.query,
                    results=[],
                    retrieved_at=datetime.now(),
                    has_results=False
                )
                results.append(error_response)
                failed_queries += 1

        # Create batch response
        batch_response = BatchRetrievalResponse(
            results=results
        )

        total_time = time.time() - start_time
        logger.info(f"Batch API request completed | Total time: {total_time:.3f}s | Batch size: {len(request.queries)} | Successful: {successful_queries} | Failed: {failed_queries}")

        return batch_response

    except HTTPException:
        total_time = time.time() - start_time
        logger.warning(f"HTTP exception in batch API request | Total time: {total_time:.3f}s | Batch size: {len(request.queries)}")
        raise
    except Exception as e:
        total_time = time.time() - start_time
        logger.error(f"Unexpected error in batch API request: {str(e)} | Total time: {total_time:.3f}s | Batch size: {len(request.queries)}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during batch content retrieval"
        )

# Add the middleware after the endpoints, or better yet, don't include it in the router
# since middleware is typically added at the app level