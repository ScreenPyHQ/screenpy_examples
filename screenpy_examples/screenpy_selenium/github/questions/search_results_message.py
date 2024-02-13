"""
A Question for finding out the displayed search results message.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy import beat

from screenpy_examples.screenpy_selenium.github.ui.github_search_results_page import (
    RESULTS_MESSAGE,
)
from screenpy_selenium import Text

if TYPE_CHECKING:
    from screenpy import Actor


class SearchResultsMessage:
    """Find the text of the search results message.

    Abilities Required:
        BrowseTheWeb

    Examples::

        the_actor.should(
            See.the(SearchResultsMessage(), ReadsExactly("1 repository result")),
        )
    """

    @beat("{} checks the results message...")
    def answered_by(self, the_actor: Actor) -> str:
        """Direct the Actor to read off the text of the results message."""
        return Text.of(RESULTS_MESSAGE).answered_by(the_actor)
