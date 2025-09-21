#!/usr/bin/env python3
"""Unit and integration tests for client module."""

import unittest
from typing import Dict, List
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock, Mock
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos
import requests


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @parameterized.expand([
        ("google", {"payload": True}),
        ("abc", {"payload": False}),
    ])
    @patch("client.get_json")
    def test_org(self, org: str, resp: Dict, mock_get_json: Mock) -> None:
        """Test org property fetches correct data."""
        mock_get_json.return_value = resp
        client = GithubOrgClient(org)
        self.assertEqual(client.org, resp)
        expected_url = GithubOrgClient.ORG_URL.format(org=org)
        mock_get_json.assert_called_once_with(expected_url)

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org: PropertyMock) -> None:
        """Test _public_repos_url returns correct repos URL."""
        expected_url = "https://api.github.com/users/google/repos"
        mock_org.return_value = {"repos_url": expected_url}
        
        client = GithubOrgClient("google")
        result = client._public_repos_url
        
        self.assertEqual(result, expected_url)
        mock_org.assert_called_once()

    @patch("client.get_json")
    @patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock)
    def test_public_repos(
        self,
        mock_public: PropertyMock,
        mock_get_json: Mock,
    ) -> None:
        """Test public_repos returns correct repo names."""
        test_payload = [
            {
                "id": 7938102,
                "name": "truth",
                "private": False,
                "owner": {"login": "google", "id": 1342004},
                "license": {"key": "bsd-3-clause"}
            },
            {
                "id": 616290,
                "name": "guava",
                "private": False,
                "owner": {"login": "google", "id": 1342004},
                "license": {"key": "apache-2.0"}
            }
        ]
        mock_public.return_value = "https://api.github.com/users/google/repos"
        mock_get_json.return_value = test_payload

        client = GithubOrgClient("google")
        result = client.public_repos()
        self.assertEqual(result, ["truth", "guava"])
        mock_get_json.assert_called_once()
        mock_public.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "bsd-3-clause"}}, "bsd-3-clause", True),
        ({"license": {"key": "bsl-1.0"}}, "bsd-3-clause", False),
        ({"license": None}, "bsd-3-clause", False),
        ({}, "bsd-3-clause", False)
    ])
    def test_has_license(self, repo: Dict, key: str, expected: bool) -> None:
        """Test has_license correctly identifies license presence."""
        client = GithubOrgClient("google")
        result = client.has_license(repo, key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient with mocked HTTP requests."""

    @classmethod
    def setUpClass(cls) -> None:
        """Configure HTTP mocks for integration tests."""
        cls.route_payloads = {
            "https://api.github.com/orgs/google": cls.org_payload,
            "https://api.github.com/orgs/google/repos": cls.repos_payload,
        }

        def mock_requests_get(url: str, *args, **kwargs):
            """Mock requests.get with appropriate payloads."""
            if url in cls.route_payloads:
                mock_response = Mock()
                mock_response.json.return_value = cls.route_payloads[url]
                mock_response.status_code = 200
                return mock_response
            raise requests.exceptions.HTTPError(f"Unexpected URL: {url}")

        cls.get_patcher = patch("requests.get", side_effect=mock_requests_get)
        cls.get_patcher.start()

    def test_public_repos_without_filter(self) -> None:
        """Test public_repos returns all public repos without license filter."""
        client = GithubOrgClient("google")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license_filter(self) -> None:
        """Test public_repos filters repos by specific license."""
        client = GithubOrgClient("google")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)

    def test_public_repos_handles_empty_license_filter(self) -> None:
        """Test public_repos with empty license string returns all repos."""
        client = GithubOrgClient("google")
        result = client.public_repos(license="")
        self.assertEqual(result, self.expected_repos)

    @classmethod
    def tearDownClass(cls) -> None:
        """Clean up HTTP mocks after integration tests."""
        cls.get_patcher.stop()


if __name__ == "__main__":
    unittest.main()