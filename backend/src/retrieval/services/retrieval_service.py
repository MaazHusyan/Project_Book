"""
Interface for retrieval functionality
"""
from abc import ABC, abstractmethod
from typing import List, Optional
import time
import logging
from ..models.query_models import Query, QueryContext
from ..models.content_models import RetrievedContent
from ..utils.cache import retrieval_cache

logger = logging.getLogger(__name__)


class RetrievalServiceInterface(ABC):
    """
    Abstract interface for retrieval functionality
    """

    @abstractmethod
    async def retrieve_content(self, query: Query, top_k: int = 5) -> List[RetrievedContent]:
        """
        Retrieve relevant content based on the query

        Args:
            query: The user's query with context
            top_k: Number of top results to return

        Returns:
            List of retrieved content with relevance scores
        """
        pass

    @abstractmethod
    async def retrieve_content_batch(self, queries: List[Query], top_k: int = 5) -> List[List[RetrievedContent]]:
        """
        Retrieve relevant content for multiple queries

        Args:
            queries: List of user queries
            top_k: Number of top results to return for each query

        Returns:
            List of lists of retrieved content for each query
        """
        pass

    @abstractmethod
    async def validate_query(self, query: Query) -> bool:
        """
        Validate the query before processing

        Args:
            query: The query to validate

        Returns:
            True if query is valid, False otherwise
        """
        pass


class RetrievalService(RetrievalServiceInterface):
    """
    Implementation of retrieval service that integrates with Qdrant
    """

    def __init__(self):
        """
        Initialize the retrieval service
        """
        from ..utils.qdrant_retriever import QdrantRetriever
        from ..config import RetrievalConfig

        self.config = RetrievalConfig()
        self.qdrant_retriever = QdrantRetriever()

    async def retrieve_content(self, query: Query, top_k: int = 5) -> List[RetrievedContent]:
        """
        Retrieve relevant content based on the query
        """
        start_time = time.time()
        logger.info(f"Starting content retrieval for query: {query.text[:50]}...")

        # Validate the query first
        if not await self.validate_query(query):
            validation_time = time.time() - start_time
            logger.warning(f"Query validation failed for: {query.text[:50]}... | Validation time: {validation_time:.3f}s")
            raise ValueError("Invalid query provided")

        # Create cache key based on query text, top_k, and context filters
        cache_key = f"retrieval_{query.text}_{top_k}_{str(query.context.filters if query.context else {})}"

        # Try to get from cache first
        cached_result = retrieval_cache.get(cache_key)
        if cached_result is not None:
            cache_hit_time = time.time() - start_time
            logger.info(f"Cache hit for query: {query.text[:50]}... | Cache retrieval time: {cache_hit_time:.3f}s")
            return cached_result

        # Enhance query with context if available
        enhanced_query_text = await self._enhance_query_with_context(query)
        context_enhancement_time = time.time() - start_time
        logger.debug(f"Query enhanced with context | Enhancement time: {context_enhancement_time:.3f}s")

        # Ensure top_k is within bounds
        top_k = min(top_k, self.config.MAX_TOP_K)

        # Use QdrantRetriever to get content
        results = await self.qdrant_retriever.search(
            query_text=enhanced_query_text,
            top_k=top_k,
            filters=query.context.filters if query.context else None
        )
        search_time = time.time() - start_time - context_enhancement_time
        logger.debug(f"Qdrant search completed | Search time: {search_time:.3f}s")

        # Apply relevance filtering
        from ..utils.relevance_calculator import RelevanceCalculator
        calculator = RelevanceCalculator()

        # Determine relevance threshold based on context
        relevance_threshold = await self._get_contextual_relevance_threshold(query)
        threshold_calc_time = time.time() - start_time - context_enhancement_time - search_time
        logger.debug(f"Relevance threshold calculated | Threshold: {relevance_threshold:.3f} | Calculation time: {threshold_calc_time:.3f}s")

        # Filter results based on relevance score (contextual or default)
        filtered_results = calculator.filter_by_min_score(results, relevance_threshold)
        filter_time = time.time() - start_time - context_enhancement_time - search_time - threshold_calc_time
        logger.debug(f"Results filtered by relevance | Filter time: {filter_time:.3f}s")

        # Sort by relevance score
        sorted_results = calculator.rank_by_relevance(filtered_results)
        sort_time = time.time() - start_time - context_enhancement_time - search_time - threshold_calc_time - filter_time
        logger.debug(f"Results sorted by relevance | Sort time: {sort_time:.3f}s")

        total_time = time.time() - start_time
        logger.info(f"Content retrieval completed | Total time: {total_time:.3f}s | Results found: {len(sorted_results)} | Query: {query.text[:50]}...")

        # Cache the results for future requests (only cache if we got results)
        if sorted_results:
            # Cache for 10 minutes
            retrieval_cache.set(cache_key, sorted_results, ttl=600)
            logger.debug(f"Results cached for query: {query.text[:50]}... | Cache TTL: 600s")

        # Performance metrics logging
        logger.debug(f"Performance metrics - Total: {total_time:.3f}s | Context: {context_enhancement_time:.3f}s | Search: {search_time:.3f}s | Filter: {filter_time:.3f}s | Sort: {sort_time:.3f}s")

        # If no relevant content is found, return empty list
        # This is handled gracefully by returning an empty list
        return sorted_results

    async def _enhance_query_with_context(self, query: Query) -> str:
        """
        Enhance the query with conversation context for better retrieval

        Args:
            query: The original query with context

        Returns:
            Enhanced query text incorporating context
        """
        base_query = query.text

        # If there's conversation history, incorporate relevant context
        if query.context and query.context.conversation_history:
            # Get the last few messages to provide context
            recent_messages = query.context.conversation_history[-3:]  # Last 3 messages

            context_parts = []
            for msg in recent_messages:
                role = getattr(msg, 'role', 'unknown')
                content = getattr(msg, 'content', '')
                if content:
                    context_parts.append(f"{role}: {content}")

            if context_parts:
                # Combine context with the current query
                context_str = " | ".join(context_parts)
                enhanced_query = f"Context: {context_str} | Current Query: {base_query}"
                return enhanced_query

        # If there's selected text, incorporate it
        if query.context and query.context.selected_text:
            selected_text = query.context.selected_text
            enhanced_query = f"Focus on: {selected_text} | Query: {base_query}"
            return enhanced_query

        # If there are specific filters, mention them in the query
        if query.context and query.context.filters:
            filters = query.context.filters
            if 'source_file' in filters:
                source_file = filters['source_file']
                enhanced_query = f"From {source_file}: {base_query}"
                return enhanced_query

        # Return original query if no context to enhance
        return base_query

    async def _get_contextual_relevance_threshold(self, query: Query) -> float:
        """
        Determine the relevance threshold based on query context.
        In some contexts, we might want to be more or less strict about relevance.

        Args:
            query: The query with context

        Returns:
            Relevance threshold to use for filtering
        """
        # Default threshold from config
        base_threshold = self.config.MIN_RELEVANCE_SCORE

        # If there's conversation history and this seems like a follow-up question,
        # potentially use a slightly lower threshold to find related content
        if (query.context and query.context.conversation_history and
            len(query.context.conversation_history) > 0):
            # Check if this query might be a follow-up (simple heuristic)
            current_query_lower = query.text.lower()
            followup_indicators = ["what", "how", "why", "where", "when", "which", "who", "explain", "describe"]

            if any(indicator in current_query_lower for indicator in followup_indicators):
                # For follow-up questions, potentially lower the threshold slightly
                # to find related content that might not be an exact match
                return max(0.3, base_threshold - 0.1)  # Don't go below 0.3

        # If specific filters are applied (like source file), we might want to be more lenient
        if query.context and query.context.filters and 'source_file' in query.context.filters:
            # When filtering by source, content is already constrained, so be slightly more lenient
            return max(0.3, base_threshold - 0.05)

        # If there's selected text, we might want to be more strict as the user has specified focus
        if query.context and query.context.selected_text:
            # When user has selected specific text, be more strict about relevance
            return min(0.8, base_threshold + 0.1)  # Don't go above 0.8

        return base_threshold

    async def retrieve_content_batch(self, queries: List[Query], top_k: int = 5) -> List[List[RetrievedContent]]:
        """
        Retrieve relevant content for multiple queries
        """
        start_time = time.time()
        logger.info(f"Starting batch content retrieval for {len(queries)} queries")

        results = []
        individual_times = []

        for i, query in enumerate(queries):
            query_start_time = time.time()
            try:
                result = await self.retrieve_content(query, top_k)
                query_time = time.time() - query_start_time
                individual_times.append(query_time)
                results.append(result)
                logger.debug(f"Batch query {i+1}/{len(queries)} completed in {query_time:.3f}s")
            except Exception as e:
                logger.error(f"Error retrieving content for batch query {i+1}: {str(e)}")
                # Return empty result for failed query to maintain result structure
                results.append([])
                individual_times.append(time.time() - query_start_time)

        total_time = time.time() - start_time
        avg_time_per_query = sum(individual_times) / len(individual_times) if individual_times else 0
        logger.info(f"Batch retrieval completed | Total time: {total_time:.3f}s | Avg per query: {avg_time_per_query:.3f}s | Queries: {len(queries)}")

        return results

    async def get_session_context(self, session_id: str) -> QueryContext:
        """
        Retrieve conversation context for a specific session
        This is a placeholder implementation - in a real system,
        this would fetch from a persistent store like Redis or database
        """
        # In a real implementation, this would fetch session context from storage
        # For now, returning an empty context
        return QueryContext()

    async def save_session_context(self, session_id: str, context: QueryContext):
        """
        Save conversation context for a specific session
        This is a placeholder implementation - in a real system,
        this would save to a persistent store like Redis or database
        """
        # In a real implementation, this would save session context to storage
        # For now, just a placeholder
        pass

    async def validate_query(self, query: Query) -> bool:
        """
        Validate the query before processing
        """
        if not query.text or not query.text.strip():
            return False

        if len(query.text.strip()) < 3:  # Minimum query length
            return False

        # Check for potentially harmful content (basic security validation)
        suspicious_patterns = ['<script', 'javascript:', 'vbscript:', 'onerror', 'onclick']
        query_lower = query.text.lower()
        for pattern in suspicious_patterns:
            if pattern in query_lower:
                return False

        return True