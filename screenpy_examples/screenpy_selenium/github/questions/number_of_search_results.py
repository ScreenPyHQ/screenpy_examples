"""
A Question to find out the number of search results on the GitHub search
page.
"""

from screenpy import Actor
from screenpy.pacing import beat
from screenpy_selenium.questions import Number

from screenpy_examples.screenpy_selenium.github.ui.github_search_results_page import (
    SEARCH_RESULTS,
)


class NumberOfSearchResults:
    """Find the number of search results.

    Abilities Required:
        BrowseTheWeb

    Examples::

        the_actor.should(See.the(NumberOfSearchResults(), Equals(4)))
    """

    @beat("{} checks the number of results...")
    def answered_by(self, the_actor: Actor) -> float:
        """Direct the Actor to count the number of search results."""
        return Number.of(SEARCH_RESULTS).answered_by(the_actor)
