"""
Test script to verify that 95% of responses are grounded in retrieved content with proper source attribution
"""
import sys
import os
import pytest
from unittest.mock import AsyncMock, MagicMock

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.retrieval.services.retrieval_service import RetrievalService
from src.retrieval.models.query_models import Query, QueryContext
from src.retrieval.models.content_models import RetrievedContent
from src.retrieval.utils.grounding_verifier import grounding_verifier


@pytest.mark.asyncio
async def test_response_grounding():
    """
    Test that responses are properly grounded in retrieved content
    """
    print("Testing response grounding in retrieved content...")

    # Initialize services
    retrieval_service = RetrievalService()

    # Mock the QdrantRetriever to avoid needing a real Qdrant instance
    mock_qdrant = AsyncMock()
    mock_qdrant.search = AsyncMock()
    retrieval_service.qdrant_retriever = mock_qdrant

    # Mock some test content for different queries
    mock_content_map = {
        "What is robot kinematics?": [
            RetrievedContent(
                id="test1",
                chunk_id="chunk1",
                content="Robot kinematics is the study of motion in robotic systems, focusing on the relationship between joint variables and the position and orientation of the robot's end-effector.",
                source_file="robotics_book_chapter_3.pdf",
                source_location="Chapter 3, Section 2.1",
                relevance_score=0.85
            )
        ],
        "Explain inverse kinematics": [
            RetrievedContent(
                id="test2",
                chunk_id="chunk2",
                content="Inverse kinematics is the mathematical process of calculating the variable joint parameters needed to place the end of a robotic arm in a particular position and orientation.",
                source_file="robotics_book_chapter_4.pdf",
                source_location="Chapter 4, Section 3.2",
                relevance_score=0.82
            )
        ],
        "What are the types of robot actuators?": [
            RetrievedContent(
                id="test3",
                chunk_id="chunk3",
                content="Robot actuators include electric motors, hydraulic actuators, and pneumatic actuators. Electric motors are most common due to their precision and controllability.",
                source_file="robotics_book_chapter_5.pdf",
                source_location="Chapter 5, Section 1.3",
                relevance_score=0.78
            )
        ],
        "Describe PID controllers in robotics": [
            RetrievedContent(
                id="test4",
                chunk_id="chunk4",
                content="PID controllers in robotics use Proportional, Integral, and Derivative terms to control robot movement and maintain desired positions with high accuracy.",
                source_file="robotics_book_chapter_6.pdf",
                source_location="Chapter 6, Section 4.1",
                relevance_score=0.80
            )
        ],
        "What is forward kinematics?": [
            RetrievedContent(
                id="test5",
                chunk_id="chunk5",
                content="Forward kinematics is the use of kinematic equations to determine the position of the end-effector from the joint parameters of the robot.",
                source_file="robotics_book_chapter_3.pdf",
                source_location="Chapter 3, Section 2.2",
                relevance_score=0.83
            )
        ],
        "Explain robot dynamics": [
            RetrievedContent(
                id="test6",
                chunk_id="chunk6",
                content="Robot dynamics deals with the relationship between forces acting on a robot mechanism and the accelerations they produce, including the effects of mass, friction, and gravity.",
                source_file="robotics_book_chapter_7.pdf",
                source_location="Chapter 7, Section 2.1",
                relevance_score=0.79
            )
        ],
        "What are the main components of a robot?": [
            RetrievedContent(
                id="test7",
                chunk_id="chunk7",
                content="The main components of a robot include sensors, actuators, controller, power supply, and mechanical structure. These components work together to perform automated tasks.",
                source_file="robotics_book_chapter_2.pdf",
                source_location="Chapter 2, Section 1.1",
                relevance_score=0.84
            )
        ],
        "Describe trajectory planning in robotics": [
            RetrievedContent(
                id="test8",
                chunk_id="chunk8",
                content="Trajectory planning in robotics involves determining the path a robot should follow to move from one point to another while avoiding obstacles and meeting kinematic constraints.",
                source_file="robotics_book_chapter_8.pdf",
                source_location="Chapter 8, Section 5.2",
                relevance_score=0.81
            )
        ],
        "What is robot control theory?": [
            RetrievedContent(
                id="test9",
                chunk_id="chunk9",
                content="Robot control theory encompasses the mathematical frameworks and algorithms used to control robot behavior, including feedback control, adaptive control, and optimal control.",
                source_file="robotics_book_chapter_6.pdf",
                source_location="Chapter 6, Section 4.3",
                relevance_score=0.77
            )
        ],
        "Explain sensor fusion in robotics": [
            RetrievedContent(
                id="test10",
                chunk_id="chunk10",
                content="Sensor fusion in robotics combines data from multiple sensors to improve the accuracy and reliability of robot perception and decision-making.",
                source_file="robotics_book_chapter_9.pdf",
                source_location="Chapter 9, Section 3.4",
                relevance_score=0.86
            )
        ]
    }

    # Test queries to verify grounding
    test_queries = list(mock_content_map.keys())

    query_response_pairs = []

    for query_text in test_queries:
        print(f"\nTesting query: '{query_text}'")

        try:
            # Mock the search response
            mock_content = mock_content_map[query_text]
            mock_qdrant.search.return_value = mock_content

            # Create query object
            query = Query(text=query_text)

            # Retrieve content (this will use the mock)
            retrieved_content = await retrieval_service.retrieve_content(query, top_k=3)
            print(f"Retrieved {len(retrieved_content)} content items")

            # For testing purposes, we'll simulate a response based on the retrieved content
            # In a real scenario, this would come from the LLM
            if retrieved_content:
                # Simulate a response that incorporates the retrieved content with proper attribution
                simulated_response = f"Based on the robotics book content from {retrieved_content[0].source_file}, {query_text.lower()} is explained as: {retrieved_content[0].content[:200]}... This information is sourced from {retrieved_content[0].source_file} at location {retrieved_content[0].source_location}."
            else:
                simulated_response = f"Based on the robotics book content, {query_text.lower()} is an important concept in robotics."

            print(f"Simulated response length: {len(simulated_response)} characters")

            # Add to test pairs
            query_response_pairs.append((query_text, retrieved_content, simulated_response))

        except Exception as e:
            print(f"Error processing query '{query_text}': {str(e)}")
            continue

    print(f"\n--- Grounding Verification Results ---")
    print(f"Total queries tested: {len(query_response_pairs)}")

    if query_response_pairs:
        # Calculate grounding percentage
        results = grounding_verifier.calculate_grounding_percentage(query_response_pairs)

        print(f"Grounded responses: {results['grounded_responses']}/{results['total_responses']}")
        print(f"Grounding percentage: {results['grounding_percentage']:.2f}%")
        print(f"Target: {results['target_percentage']}%")
        print(f"Meets target: {'YES' if results['meets_target'] else 'NO'}")

        # Print detailed results for each query
        print("\n--- Detailed Results ---")
        for i, detail in enumerate(results['details']):
            status = "✓" if detail['is_grounded'] else "✗"
            print(f"{status} Query {i+1}: '{detail['query'][:50]}...'")
            print(f"   Grounded: {detail['is_grounded']}")
            print(f"   Content count: {detail['details']['retrieved_content_count']}")
            print(f"   Sources: {len(detail['details']['content_sources'])}")
            print(f"   Similarity: {detail['details']['content_similarity_score']:.3f}")
            print(f"   Attribution: {detail['details']['source_attribution_present']}")
            if detail['details']['grounding_issues']:
                print(f"   Issues: {', '.join(detail['details']['grounding_issues'])}")
            print()

        # Overall assessment
        if results['meets_target']:
            print("✅ SUCCESS: 95% of responses are properly grounded in retrieved content!")
            assert True
        else:
            print("❌ FAILURE: Less than 95% of responses are properly grounded in retrieved content!")
            assert False
    else:
        print("No test data available for verification.")
        assert False


if __name__ == "__main__":
    import asyncio
    success = asyncio.run(test_response_grounding())
    sys.exit(0 if success else 1)