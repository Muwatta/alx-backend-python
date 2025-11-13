#!/usr/bin/env python3
"""
Module for utility functions: nested map access, JSON requests, and memoization.
"""

from typing import Any, Callable
import requests


def access_nested_map(nested_map: dict, path: tuple) -> Any:
    current = nested_map
    for key in path:
        if not isinstance(current, dict) or key not in current:
            raise KeyError(key)
        current = current[key]
    return current


def get_json(url: str) -> dict:
    response = requests.get(url)
    return response.json()


def memoize(func: Callable) -> Callable:
    cache = {}

    def wrapper(self):
        if func not in cache:
            cache[func] = func(self)
        return cache[func]

    return wrapper
