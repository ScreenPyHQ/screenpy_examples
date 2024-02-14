"""
Locators for the GitHub search results page.
"""

from __future__ import annotations

from screenpy_selenium import Target

RESULTS_MESSAGE = Target.the("search results message").located_by(
    "div.codesearch-results > div > div > h3"  # ew
)
SEARCH_RESULTS = Target.the("search results items").located_by("li.repo-list-item")
