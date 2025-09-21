#!/usr/bin/env python3
"""Utility module for nested map access, JSON fetching, and memoization."""

from typing import Mapping, Sequence, Any, Dict, Callable
import requests


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access a value in a nested dictionary using a sequence of keys.

    Args:
        nested_map (Mapping): The nested dictionary to traverse.
        path (Sequence): The sequence of keys to follow.

    Returns:
        Any: The value at the end of the path.

    Raises:
        KeyError: If a key in the path is missing or inaccessible.
    """
    for key in path:
        try:
            nested_map = nested_map[key]
        except (KeyError, TypeError):
            raise KeyError(key)
    return nested_map


def get_json(url: str) -> Dict:
    """Fetch JSON data from a given URL.

    Args:
        url (str): The URL to fetch from.

    Returns:
        Dict: The JSON payload from the response.
    """
    response = requests.get(url)
    return response.json()


def memoize(fn: Callable) -> Callable:
    """Decorator to memoize a method as a cached property.

    Args:
        fn (Callable): The method to memoize.

    Returns:
        Callable: A property that caches the result of the method.
    """
    attr_name = f"_{fn.__name__}"

    @property
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return wrapper
