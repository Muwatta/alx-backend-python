#!/usr/bin/env python3
"""GitHub organization client module."""

from typing import List, Dict, Optional, Any
from utils import get_json


class GithubOrgClient:
    """Client for fetching GitHub organization data.

    Attributes:
        ORG_URL (str): Template URL for GitHub org API.
    """
    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name: str) -> None:
        """Initialize the client with the organization name.

        Args:
            org_name (str): The GitHub organization name.
        """
        self._org_name = org_name

    @property
    def org(self) -> Dict:
        """Fetch and return the organization data.

        Returns:
            Dict: The organization's JSON data.
        """
        return get_json(self.ORG_URL.format(org=self._org_name))

    @property
    def _public_repos_url(self) -> str:
        """Get the URL for public repositories.

        Returns:
            str: The repos URL from org data.
        """
        return self.org["repos_url"]

    def public_repos(self, license: Optional[str] = None) -> List[str]:
        """Get list of public repo names, optionally filtered by license.

        Args:
            license (Optional[str]): License key to filter by.

        Returns:
            List[str]: List of repo names.
        """
        json_repos = get_json(self._public_repos_url)
        
        # Treat empty string as no filter (same as None)
        if license == "":
            license = None
            
        return [
            repo["name"] for repo in json_repos
            if license is None or self.has_license(repo, license)
        ]

    @staticmethod
    def has_license(repo: Dict[str, Any], license_key: str) -> bool:
        """Check if a repo has a specific license.

        Args:
            repo (Dict[str, Any]): The repo data.
            license_key (str): The license key to check.

        Returns:
            bool: True if the license matches.
        """
        if "license" not in repo or repo["license"] is None:
            return False
        return repo["license"].get("key") == license_key
