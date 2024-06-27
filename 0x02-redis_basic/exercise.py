#!/usr/bin/env python3
""" 12-log_stats.py """
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """increments the count for that key every time the method"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """doc"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """store the input and output"""
    @wraps(method)
    def wrapper(self, *args):
        """doc"""
        if isinstance(self._redis, redis.Redis):
            methodname = method.__qualname__
            keyin = methodname + ":inputs"
            keyout = methodname + ":outputs"
            input = str(args)
            self._redis.rpush(keyin, input)
            output = method(self, *args)
            self._redis.rpush(keyout, output)
        return output
    return wrapper


class Cache:
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ store """
        id = str(uuid.uuid4())
        self._redis.set(id, data)
        return id

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """convert the data back to the desired format"""
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """automatically parametrize Cache.get with the correct
        conversion function"""
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        """automatically parametrize Cache.get with the correct
        conversion function"""
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value
