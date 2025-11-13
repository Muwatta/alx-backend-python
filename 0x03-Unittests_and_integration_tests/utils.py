#!/usr/bin/env python3
"""
Module for utility functions: nested map access, JSON requests, and memoization.
"""

from typing import Any, Callable
import requests


def access_nested_map(nested_map: dict, path: tuple) -> Any:
    """
    Access a value in a nested map using a tuple path.

    Args:
        nested_map (dict): The dictionary to access.
        path (tuple): Keys to traverse in order.

    Returns:
        Any: Value found at the path.

    Raises:
        KeyError: If any key in the path is missing.
    """
    current = nested_map
    for key in path:
        if key not in current:
            raise KeyError(key)
        current = current[key]
    return current


def get_json(url: str) -> dict:
    """
    Make an HTTP GET request to the given URL and return JSON response.

    Args:
        url (str): The URL to fetch.

    Returns:
        dict: JSON response from the server.
    """
    response = requests.get(url)
    return response.json()


def memoize(func: Callable) -> property:
    """
    Decorator to cache the result of a method with no arguments.
    Converts the method into a property.

    Args:
        func (Callable): Method to memoize.

    Returns:
        property: Property that caches its result.
    """
    cache = {}

    def wrapper(self):
        if func not in cache:
            cache[func] = func(self)
        return cache[func]

    return property(wrapper)
