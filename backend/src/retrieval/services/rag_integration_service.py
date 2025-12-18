"""
Integration service for connecting retrieval functionality with chatbot agent
"""
import time
import logging
from typing import List, Optional
from ..models.query_models import Query
from ..models.content_models import RetrievedContent
from .retrieval_service import RetrievalService

logger = logging.getLogger(__name__)


class RAGIntegrationService:
    """
    Service for integrating retrieval functionality with chatbot agent
    """

    def __init__(self):
        """
        Initialize the RAG integration service
        """
        self.retrieval_service = RetrievalService()

    async def get_relevant_content_for_query(
        self,
        query_text: str,
        session_id: Optional[str] = None,
        top_k: int = 5
    ) -> List[RetrievedContent]:
        """
        Get relevant content for a user query to be used by the chatbot agent

        Args:
            query_text: The user's query text
            session_id: Optional session identifier for context
            top_k: Number of top results to return

        Returns:
            List of relevant content to be used for response generation
        """
        start_time = time.time()
        logger.info(f"Getting relevant content for query: {query_text[:50]}... | Session: {session_id}")

        # Create a Query object from the input
        query = Query(
            text=query_text,
            session_id=session_id
        )

        # Use the retrieval service to get relevant content
        results = await self.retrieval_service.retrieve_content(
            query=query,
            top_k=top_k
        )

        total_time = time.time() - start_time
        logger.info(f"Got {len(results)} relevant content items | Total time: {total_time:.3f}s | Query: {query_text[:50]}...")

        return results

    async def get_relevant_content_with_context(
        self,
        query_text: str,
        conversation_context: List[dict] = None,
        filters: dict = None,
        top_k: int = 5
    ) -> List[RetrievedContent]:
        """
        Get relevant content considering conversation context

        Args:
            query_text: The user's query text
            conversation_context: List of previous conversation turns
            filters: Additional filters to apply
            top_k: Number of top results to return

        Returns:
            List of relevant content considering the context
        """
        start_time = time.time()
        logger.info(f"Getting relevant content with context for query: {query_text[:50]}... | Context turns: {len(conversation_context) if conversation_context else 0}")

        from ..models.query_models import QueryContext

        # Create context from conversation history
        query_context = QueryContext()
        if conversation_context:
            query_context.conversation_history = conversation_context
        if filters:
            query_context.filters = filters

        # Create a Query object with context
        query = Query(
            text=query_text,
            context=query_context
        )

        # Use the retrieval service to get relevant content
        results = await self.retrieval_service.retrieve_content(
            query=query,
            top_k=top_k
        )

        total_time = time.time() - start_time
        logger.info(f"Got {len(results)} relevant content items with context | Total time: {total_time:.3f}s | Query: {query_text[:50]}...")

        return results

    async def validate_content_relevance(
        self,
        query_text: str,
        retrieved_content: List[RetrievedContent],
        min_relevance_score: float = 0.5
    ) -> bool:
        """
        Validate if the retrieved content is relevant to the query

        Args:
            query_text: The original query text
            retrieved_content: List of retrieved content
            min_relevance_score: Minimum relevance score threshold

        Returns:
            True if content is relevant, False otherwise
        """
        if not retrieved_content:
            return False

        # Check if any content meets the relevance threshold
        for content in retrieved_content:
            if content.relevance_score >= min_relevance_score:
                return True

        return False