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
    """store the history of inputs and outputs"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper for the decorated function"""
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output

    return wrapper


def replay(method: Callable) -> None:
    """ replay the history """
    redis_client = redis.Redis()
    methodname = method.__qualname__
    listin = redis_client.lrange(f"{methodname}:inputs", 0, -1)  # nopep8
    listout = redis_client.lrange(f"{methodname}:outputs", 0, -1)  # nopep8

    in_and_out = zip(listin, listout)
    in_and_out_list = list(in_and_out)  # Store the result of zip in a list
    print(f"Cache.store was called {len(in_and_out_list)} times:")
    for invalue, outvalue in in_and_out_list:
        # Convert binary strings to regular strings
        if isinstance(invalue, bytes):
            invalue_str = f"{invalue.decode('utf-8')}"
        elif isinstance(invalue, int):
            invalue_str = f"{invalue}"
        else:
            invalue_str = f"{invalue}"

        outvalue_str = outvalue.decode('utf-8')
        print(f"{methodname}(*{invalue_str}) -> {outvalue_str}")


class Cache:
    """define a class cach"""
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
