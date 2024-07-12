#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""
import requests
from typing import Callable
from functools import wraps
import redis


def Mydecorator(fun: Callable) -> Callable:
    """ Track a web page """
    @wraps(fun)
    def wrapper(url):
        """ wrapper for a get page function """
        client = redis.Redis()
        client.incr(f'count:{url}')
        cached_page = client.get(f'{url}')
        if cached_page:
            return cached_page.decode('utf-8')
        page = fun(url)
        client.set(f'{url}', page, 10)

        return page
    return wrapper


@Mydecorator
def get_page(url: str) -> str:
    """ Implementing an expiring web cache and tracker """
    response = requests.get(url)
    return response.text
