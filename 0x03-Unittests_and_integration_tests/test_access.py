#!/usr/bin/env python3

from utils import access_nested_map

print(access_nested_map({"a": 1}, ("a",)))
print(access_nested_map({"a": {"b": 2}}, ("a", "b")))
print(access_nested_map({"a": {"b": 2}}, ("a",)))

try:
    access_nested_map({}, ("a",))
except KeyError as e:
    print(f"Caught KeyError: {e}")
