"""
Utility for verifying that responses are grounded in retrieved content with proper source attribution
"""
import logging
from typing import List, Dict, Any, Tuple
from ..models.content_models import RetrievedContent


logger = logging.getLogger(__name__)


class GroundingVerifier:
    """
    Utility class for verifying that responses are properly grounded in retrieved content
    with appropriate source attribution.
    """

    def __init__(self):
        """
        Initialize the grounding verifier
        """
        pass

    def verify_response_grounding(
        self,
        query: str,
        retrieved_content: List[RetrievedContent],
        response: str
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Verify that a response is properly grounded in the retrieved content

        Args:
            query: The original query
            retrieved_content: List of retrieved content used to generate the response
            response: The generated response to verify

        Returns:
            Tuple of (is_grounded, verification_details)
        """
        verification_details = {
            'query': query,
            'response_length': len(response),
            'retrieved_content_count': len(retrieved_content),
            'content_sources': list(set([content.source_file for content in retrieved_content if content.source_file])),
            'has_sources_in_response': False,
            'content_similarity_score': 0.0,
            'source_attribution_present': False,
            'grounding_issues': []
        }

        # Check if response is empty
        if not response.strip():
            verification_details['grounding_issues'].append('Response is empty')
            return False, verification_details

        # Check if retrieved content is empty
        if not retrieved_content:
            verification_details['grounding_issues'].append('No retrieved content to ground response')
            return False, verification_details

        # Check if response contains references to sources
        source_attribution_present = self._check_source_attribution(response, retrieved_content)
        verification_details['source_attribution_present'] = source_attribution_present

        # Check content similarity
        content_similarity_score = self._calculate_content_similarity(response, retrieved_content)
        verification_details['content_similarity_score'] = content_similarity_score

        # Check if response contains content from retrieved sources
        has_content_from_sources = self._check_content_from_sources(response, retrieved_content)
        verification_details['has_sources_in_response'] = has_content_from_sources

        # Determine if response is properly grounded
        is_grounded = (
            source_attribution_present or  # Has source attribution
            content_similarity_score > 0.3 or  # Has some similarity to retrieved content
            has_content_from_sources  # Contains content from sources
        )

        if not is_grounded:
            verification_details['grounding_issues'].append(
                'Response lacks proper grounding in retrieved content'
            )

        # Additional checks
        if content_similarity_score < 0.1:
            verification_details['grounding_issues'].append(
                'Low similarity between response and retrieved content'
            )

        return is_grounded, verification_details

    def _check_source_attribution(self, response: str, retrieved_content: List[RetrievedContent]) -> bool:
        """
        Check if the response contains source attribution

        Args:
            response: The response text
            retrieved_content: List of retrieved content

        Returns:
            True if source attribution is present
        """
        response_lower = response.lower()
        source_files = [content.source_file.lower() for content in retrieved_content if content.source_file]
        source_locations = [content.source_location.lower() for content in retrieved_content if content.source_location]

        # Check for common attribution phrases
        attribution_indicators = [
            'source:', 'sources:', 'reference:', 'references:', 'according to', 'from the',
            'cited in', 'mentioned in', 'found in', 'as stated in', 'based on'
        ]

        for indicator in attribution_indicators:
            if indicator in response_lower:
                return True

        # Check for specific source files
        for source_file in source_files:
            if source_file in response_lower:
                return True

        # Check for source locations
        for location in source_locations:
            if location in response_lower:
                return True

        return False

    def _calculate_content_similarity(self, response: str, retrieved_content: List[RetrievedContent]) -> float:
        """
        Calculate similarity between response and retrieved content

        Args:
            response: The response text
            retrieved_content: List of retrieved content

        Returns:
            Similarity score between 0 and 1
        """
        if not retrieved_content:
            return 0.0

        response_words = set(response.lower().split())
        all_content_words = set()

        for content in retrieved_content:
            content_words = set(content.content.lower().split())
            all_content_words.update(content_words)

        if not all_content_words:
            return 0.0

        # Calculate Jaccard similarity
        intersection = response_words.intersection(all_content_words)
        union = response_words.union(all_content_words)

        if len(union) == 0:
            return 0.0

        return len(intersection) / len(union)

    def _check_content_from_sources(self, response: str, retrieved_content: List[RetrievedContent]) -> bool:
        """
        Check if response contains content from retrieved sources

        Args:
            response: The response text
            retrieved_content: List of retrieved content

        Returns:
            True if response contains content from sources
        """
        response_lower = response.lower()

        for content in retrieved_content:
            content_lower = content.content.lower()
            # Check if at least 10% of the content appears in the response
            content_words = content_lower.split()
            if len(content_words) == 0:
                continue

            # Look for phrases from the content in the response
            for i in range(len(content_words)):
                # Build phrases of different lengths
                for length in [2, 3, 4, 5]:  # Check 2-5 word phrases
                    if i + length <= len(content_words):
                        phrase = ' '.join(content_words[i:i + length])
                        if len(phrase) > 10 and phrase in response_lower:  # At least 10 chars to avoid common words
                            return True

        return False

    def calculate_grounding_percentage(
        self,
        query_response_pairs: List[Tuple[str, List[RetrievedContent], str]]
    ) -> Dict[str, Any]:
        """
        Calculate the percentage of responses that are properly grounded

        Args:
            query_response_pairs: List of (query, retrieved_content, response) tuples

        Returns:
            Dictionary with grounding statistics
        """
        if not query_response_pairs:
            return {
                'total_responses': 0,
                'grounded_responses': 0,
                'grounding_percentage': 0.0,
                'details': []
            }

        total_responses = len(query_response_pairs)
        grounded_responses = 0
        details = []

        for query, retrieved_content, response in query_response_pairs:
            is_grounded, verification_details = self.verify_response_grounding(
                query, retrieved_content, response
            )
            details.append({
                'query': query,
                'is_grounded': is_grounded,
                'details': verification_details
            })

            if is_grounded:
                grounded_responses += 1

        grounding_percentage = (grounded_responses / total_responses) * 100 if total_responses > 0 else 0

        return {
            'total_responses': total_responses,
            'grounded_responses': grounded_responses,
            'grounding_percentage': grounding_percentage,
            'target_percentage': 95.0,  # Target 95% grounding
            'meets_target': grounding_percentage >= 95.0,
            'details': details
        }


# Global instance for convenience
grounding_verifier = GroundingVerifier()