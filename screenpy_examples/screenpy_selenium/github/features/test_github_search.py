"""
An example of a test module that follows the typical pytest test
structure. These tests show off how to use custom tasks and Questions,
though they are a little bit contrived.
"""

from typing import Generator

import pytest
from allure_commons.types import AttachmentType

from screenpy import Actor, given, then, when
from screenpy.actions import See
from screenpy.pacing import act, scene
from screenpy_selenium.abilities import BrowseTheWeb
from screenpy_selenium.actions import Open, SaveScreenshot
from screenpy.resolutions import (
    ContainsTheText,
    ContainTheText,
    DoesNot,
    IsEqualTo,
    ReadsExactly,
)

from ..questions.number_of_search_results import NumberOfSearchResults
from ..questions.search_results_message import SearchResultsMessage
from ..tasks.search_github import SearchGitHub
from ..ui.github_home_page import URL


@pytest.fixture(scope="function", name="Perry")
def fixture_actor() -> Generator:
    """Create the Actor for our example tests!"""
    the_actor = Actor.named("Perry").who_can(BrowseTheWeb.using_firefox())
    yield the_actor
    the_actor.attempts_to(
        SaveScreenshot.as_("test.png").and_attach_it(
            name="End of Test Screenshot", attachment_type=AttachmentType.PNG
        ),
    )
    the_actor.exit_stage_left()


@act("Search")
@scene("Search for the ScreenPy examples repository on GitHub")
def test_search_for_screenpy(Perry: Actor) -> None:
    """GitHub search finds the screenpy examples repository."""
    given(Perry).was_able_to(Open.their_browser_on(URL))
    when(Perry).attempts_to(SearchGitHub.for_text("ScreenPyHQ/screenpy_examples"))
    then(Perry).should(
        See.the(SearchResultsMessage(), DoesNot(ContainTheText("couldn’t"))),
        See.the(SearchResultsMessage(), ReadsExactly("1 repository result")),
        See.the(NumberOfSearchResults(), IsEqualTo(1)),
    )


@act("Search")
@scene("Search for a nonexistant repository on GitHub")
def test_search_for_nonexistent_repo(Perry: Actor) -> None:
    """GitHub search fails to find a nonexistant repository."""
    nonexistant_repository = "perrygoy/i-never-made-this-repo"

    given(Perry).was_able_to(Open.their_browser_on(URL))
    when(Perry).attempts_to(SearchGitHub.for_text(nonexistant_repository))
    then(Perry).should(
        See.the(SearchResultsMessage(), ContainsTheText("We couldn’t find any")),
        See.the(SearchResultsMessage(), ContainsTheText(nonexistant_repository)),
        See.the(NumberOfSearchResults(), IsEqualTo(0)),
    )
