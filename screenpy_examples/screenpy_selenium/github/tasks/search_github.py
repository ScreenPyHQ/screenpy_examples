"""
A slightly more interesting task to search GitHub for a string.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy import beat
from screenpy_selenium import Enter, Wait
from selenium.webdriver.common.keys import Keys

from screenpy_examples.screenpy_selenium.github.ui.github_header_bar import SEARCH_INPUT
from screenpy_examples.screenpy_selenium.github.ui.github_search_results_page import (
    RESULTS_MESSAGE,
)

if TYPE_CHECKING:
    from screenpy import Actor


class SearchGitHub:
    """A task to search GitHub for a specific query.

    Abilities Required:
        BrowseTheWeb

    Examples:
        the_actor.attempts_to(SearchGitHub.for_text("screenpy"))
    """

    @staticmethod
    def for_text(search_query: str) -> "SearchGitHub":
        """Supply the text to search GitHub for."""
        return SearchGitHub(search_query)

    @beat('{} searches GitHub for "{search_query}"')
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to search github for the given term."""
        the_actor.attempts_to(
            Enter.the_text(self.search_query).into(SEARCH_INPUT).then_hit(Keys.RETURN),
            Wait.for_the(RESULTS_MESSAGE),
        )

    def __init__(self, search_query: str) -> None:
        self.search_query = search_query
