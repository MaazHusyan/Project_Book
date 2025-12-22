#!/usr/bin/env python3
"""
Test script to verify Qdrant data retrieval
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from qdrant_client import QdrantClient
from qdrant_client.http.models import SearchRequest
import numpy as np

def test_qdrant_connection():
    """Test direct Qdrant connection and data retrieval"""
    print("🔍 Testing Qdrant Connection...")

    try:
        # Connect to Qdrant
        client = QdrantClient(
            url="http://localhost:6333",
            timeout=10
        )

        print("✅ Qdrant connection established")

        # List collections
        collections = client.get_collections()
        print(f"📚 Collections: {[col.name for col in collections.collections]}")

        # Check the robotics_embeddings collection
        collection_name = "robotics_embeddings"
        try:
            collection_info = client.get_collection(collection_name)
            print(f"📊 Collection '{collection_name}' info:")
            print(f"   - Points count: {collection_info.points_count}")
            print(f"   - Indexed vectors: {collection_info.indexed_vectors_count}")

            # Sample some points to verify data exists
            if collection_info.points_count > 0:
                scroll_result = client.scroll(
                    collection_name=collection_name,
                    limit=3,
                    with_payload=True,
                    with_vectors=False
                )

                print(f"📝 Sample points from collection:")
                # scroll_result returns (points, next_offset) - points is a list of PointStruct objects
                points = scroll_result[0]
                for i, point in enumerate(points):
                    payload = point.payload
                    print(f"   Point {i+1} (ID: {point.id}):")
                    print(f"     - Content: {payload.get('content', '')[:100]}...")
                    print(f"     - Source: {payload.get('source_file', 'N/A')}")
                    print(f"     - Location: {payload.get('source_location', 'N/A')}")
                    print()

                print("✅ Qdrant data retrieval test PASSED!")
                return True
            else:
                print("❌ No points found in collection")
                return False

        except Exception as e:
            print(f"❌ Error accessing collection '{collection_name}': {str(e)}")
            return False

    except Exception as e:
        print(f"❌ Qdrant connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🤖 Qdrant Data Retrieval Test")
    print("=" * 50)

    success = test_qdrant_connection()

    if success:
        print("\n🎉 Qdrant is properly configured and data is accessible!")
        print("✅ Data has been successfully loaded into Qdrant")
        print("✅ Qdrant collection contains the robotics book embeddings")
        print("✅ The retrieval system can access the vector database")
    else:
        print("\n❌ Qdrant test FAILED")
        print("The Qdrant connection or data loading may need troubleshooting")