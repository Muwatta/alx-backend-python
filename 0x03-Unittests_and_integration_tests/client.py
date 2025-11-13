#!/usr/bin/env python3
"""
Client for interacting with GitHub organization API.
"""

from typing import List, Dict
import requests
from utils import get_json, memoize


class GithubOrgClient:
    """GitHub Organization Client."""

    def __init__(self, org_name: str) -> None:
        self.org_name = org_name

    @property
    @memoize
    def org(self) -> Dict:
        """Return organization JSON data."""
        return get_json(f"https://api.github.com/orgs/{self.org_name}")

    @property
    def _public_repos_url(self) -> str:
        """Return the public repos URL for the org."""
        return self.org["repos_url"]

    def public_repos(self, license: str = None) -> List[str]:
        """Return list of public repo names, filtered by license if provided."""
        repos = get_json(self._public_repos_url)
        if license:
            repos = [r for r in repos if r.get("license", {}).get("key") == license]
        return [r["name"] for r in repos]

    @staticmethod
    def has_license(repo: Dict, license_key: str) -> bool:
        """Check if repo has a specific license."""
        return repo.get("license", {}).get("key") == license_key
