"""
Simple in-memory cache for retrieval results to improve performance
"""
import time
import hashlib
from typing import Any, Optional
from threading import Lock


class SimpleCache:
    """
    Simple in-memory cache with TTL support
    """

    def __init__(self, default_ttl: int = 300):  # 5 minutes default TTL
        """
        Initialize the cache

        Args:
            default_ttl: Default time-to-live in seconds
        """
        self._cache = {}
        self._timestamps = {}
        self._default_ttl = default_ttl
        self._lock = Lock()

    def _make_key(self, *args, **kwargs) -> str:
        """
        Create a cache key from function arguments
        """
        key_str = f"{args}_{sorted(kwargs.items())}"
        return hashlib.md5(key_str.encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        with self._lock:
            if key not in self._cache:
                return None

            timestamp = self._timestamps[key]
            if time.time() - timestamp > self._default_ttl:
                # Entry has expired
                del self._cache[key]
                del self._timestamps[key]
                return None

            return self._cache[key]

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Set a value in the cache

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (uses default if None)
        """
        ttl = ttl or self._default_ttl
        with self._lock:
            self._cache[key] = value
            self._timestamps[key] = time.time()

    def delete(self, key: str) -> None:
        """
        Delete a key from the cache

        Args:
            key: Cache key to delete
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                del self._timestamps[key]

    def clear(self) -> None:
        """
        Clear all cache entries
        """
        with self._lock:
            self._cache.clear()
            self._timestamps.clear()


# Global cache instance
retrieval_cache = SimpleCache(default_ttl=600)  # 10 minutes for retrieval results