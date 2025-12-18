"""
Custom exceptions for the RAG retrieval function
"""


class RetrievalError(Exception):
    """Base exception for retrieval-related errors"""
    pass


class QueryProcessingError(RetrievalError):
    """Raised when there's an error processing a user query"""
    pass


class ContentRetrievalError(RetrievalError):
    """Raised when there's an error retrieving content from storage"""
    pass


class InvalidQueryError(RetrievalError):
    """Raised when a query is invalid or malformed"""
    pass


class NoRelevantContentError(RetrievalError):
    """Raised when no relevant content is found for a query"""
    pass


class ContextProcessingError(RetrievalError):
    """Raised when there's an error processing conversation context"""
    pass


class APIIntegrationError(RetrievalError):
    """Raised when there's an error in API integration"""
    pass