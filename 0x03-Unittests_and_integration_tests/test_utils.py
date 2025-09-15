#!/usr/bin/env python3
"""Unit tests for utils module"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json


class TestAccessNestedMap(unittest.TestCase):
    """Test class for access_nested_map function"""

    @parameterized.expand([
        ({"a": 1},
         ("a",),
         1),
        ({"a": {"b": 2}},
         ("a",),
         {"b": 2}),
        ({"a": {"b": 2}},
         ("a", "b"),
         2),
    ])
    def test_access_nested_map(
            self, nested_map: dict, path: tuple, expected: any
    ) -> None:
        """Test access_nested_map returns expected result"""
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)

    @parameterized.expand([
        ({},
         ("a",),
         "a"),
        ({"a": 1},
         ("a", "b"),
         "b"),
    ])
    def test_access_nested_map_exception(
            self, nested_map: dict, path: tuple, expected_exception: str
    ) -> None:
        """Test access_nested_map raises KeyError for invalid paths"""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception),
                         f"'{expected_exception}'")


class TestGetJson(unittest.TestCase):
    """Test class for get_json function"""

    @parameterized.expand([
        ("http://example.com",
         {"payload": True}),
        ("http://holberton.io",
         {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url: str, test_payload: dict,
                      mock_get: Mock) -> None:
        """Test get_json returns expected payload"""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)
        self.assertEqual(result, test_payload)
        mock_get.assert_called_once_with(test_url)
