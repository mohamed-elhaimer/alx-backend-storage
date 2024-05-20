#!/usr/bin/env python3
""" 12-log_stats.py """
import redis
import uuid
from typing import Union


class Cache:
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ store """
        id = str(uuid.uuid4())
        self._redis.set(id, data)
        return id
