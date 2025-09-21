#!/usr/bin/env python3
"""Fixtures for GitHub API integration tests."""

org_payload = {
    "repos_url": "https://api.github.com/orgs/google/repos",
}

repos_payload = [
    {"name": "truth", "license": {"key": "apache-2.0"}},
    {"name": "guava", "license": {"key": "apache-2.0"}},
    {"name": "gson", "license": {"key": "apache-2.0"}},
    {"name": "dagger", "license": {"key": "apache-2.0"}},
    {"name": "auto", "license": {"key": "apache-2.0"}},
    {"name": "error-prone", "license": {"key": "apache-2.0"}},
    {"name": "jaxb", "license": None},
    {"name": "caliper", "license": {"key": "mit"}},
    {"name": "closure-compiler", "license": {"key": "apache-2.0"}},
    {"name": "closure-templates", "license": {"key": "apache-2.0"}},
]

expected_repos = [
    "truth", "guava", "gson", "dagger", "auto", "error-prone",
    "jaxb", "caliper", "closure-compiler", "closure-templates"
]

apache2_repos = [
    "truth", "guava", "gson", "dagger", "auto", "error-prone",
    "closure-compiler", "closure-templates"
]