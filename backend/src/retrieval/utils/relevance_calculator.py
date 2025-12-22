"""
Functions for calculating and filtering relevance scores
"""
from typing import List
from ..models.content_models import RetrievedContent
import math


class RelevanceCalculator:
    """
    Utility class for calculating and filtering relevance scores
    """

    @staticmethod
    def normalize_score(score: float, min_score: float = 0.0, max_score: float = 1.0) -> float:
        """
        Normalize a relevance score to the range [0, 1]

        Args:
            score: The raw score to normalize
            min_score: The minimum possible score
            max_score: The maximum possible score

        Returns:
            Normalized score between 0 and 1
        """
        if max_score == min_score:
            return 0.0

        normalized = (score - min_score) / (max_score - min_score)
        return max(0.0, min(1.0, normalized))

    @staticmethod
    def calculate_combined_relevance(
        base_score: float,
        content_length: int,
        source_relevance: float = 1.0,
        freshness_factor: float = 1.0
    ) -> float:
        """
        Calculate a combined relevance score based on multiple factors

        Args:
            base_score: The base similarity score (usually from vector search)
            content_length: Length of the retrieved content
            source_relevance: Relevance of the source (1.0 = most relevant)
            freshness_factor: How recent the content is (1.0 = most recent)

        Returns:
            Combined relevance score between 0 and 1
        """
        # Apply length normalization (prefer medium-length content over very short or very long)
        length_factor = RelevanceCalculator._length_normalization(content_length)

        # Combine all factors
        combined_score = (
            base_score * 0.5 +  # Base similarity is most important
            length_factor * 0.2 +  # Length factor
            source_relevance * 0.2 +  # Source relevance
            freshness_factor * 0.1  # Freshness factor
        )

        return RelevanceCalculator.normalize_score(combined_score, 0.0, 1.0)

    @staticmethod
    def _length_normalization(content_length: int) -> float:
        """
        Calculate a length normalization factor based on content length

        Args:
            content_length: Length of the content in characters

        Returns:
            Length normalization factor between 0 and 1
        """
        if content_length <= 0:
            return 0.0

        # Optimal content length range (in characters)
        optimal_min = 100
        optimal_max = 1000

        if optimal_min <= content_length <= optimal_max:
            # Content within optimal range gets full score
            return 1.0
        elif content_length < optimal_min:
            # Short content gets score proportional to its length
            return min(1.0, content_length / optimal_min)
        else:
            # Long content gets score based on how close it is to optimal
            # but capped at 0.8 to avoid overly long content
            return min(0.8, optimal_max / content_length)

    @staticmethod
    def filter_by_min_score(
        contents: List[RetrievedContent],
        min_score: float
    ) -> List[RetrievedContent]:
        """
        Filter retrieved contents by minimum relevance score

        Args:
            contents: List of retrieved contents
            min_score: Minimum score threshold

        Returns:
            Filtered list of contents
        """
        return [content for content in contents if content.relevance_score >= min_score]

    @staticmethod
    def rank_by_relevance(contents: List[RetrievedContent]) -> List[RetrievedContent]:
        """
        Sort retrieved contents by relevance score in descending order

        Args:
            contents: List of retrieved contents

        Returns:
            List of contents sorted by relevance score
        """
        return sorted(contents, key=lambda x: x.relevance_score, reverse=True)

    @staticmethod
    def apply_relevance_threshold(
        contents: List[RetrievedContent],
        threshold: float = 0.5
    ) -> List[RetrievedContent]:
        """
        Apply a relevance threshold to filter out low-quality results

        Args:
            contents: List of retrieved contents
            threshold: Minimum relevance score threshold

        Returns:
            Filtered list of contents above the threshold
        """
        return [content for content in contents if content.relevance_score >= threshold]