"""
Locators for elements in the GitHub header bar.
"""

from screenpy_selenium import Target

SEARCH_INPUT = Target.the("GitHub header's search input").located_by(
    "input.header-search-input"
)
