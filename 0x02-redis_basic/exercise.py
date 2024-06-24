#!/usr/bin/env python3
""" 12-log_stats.py """
import redis
import uuid
from typing import Union, callable, Optional


class Cache:
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ store """
        id = str(uuid.uuid4())
        self._redis.set(id, data)
        return id

    def get(self, key: str, fn: Optional[callable] = None) -> Union[str, bytes, int, float]:
        """convert the data back to the desired format."""
        value = self._redis.get(key)
        if fn:
            value = fn(value)
            return value
        return value
    def get_str(self, key: str) -> Optional[str]:
        """get_str"""
        return self.get(key, lambda x: x.decode("utf-8"))
    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer value from Redis.

        Args:
            key (str): The key of the integer to retrieve.

        Returns:
            Optional[int]: The integer value, or None if key does not exist.
        """
        return self.get(key, lambda x: int(x))
