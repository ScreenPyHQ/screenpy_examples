"""
An example of a test module that follows the typical unittest.TestCase
test structure. These tests exercise the Wait and Enter Actions.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Callable, Tuple

from screenpy import Actor
from screenpy.actions import See
from screenpy.pacing import act, scene
from screenpy.resolutions import ReadsExactly
from screenpy_selenium.actions import Enter, Open, Wait
from screenpy_selenium.questions import Text

from ..user_interface.key_presses import ENTRY_INPUT, RESULT_TEXT, URL

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver


class TestKeyPresses:
    """
    Flexes Waiting with various strategies.
    """

    @act("Perform")
    @scene("Wait for text")
    def test_wait_for_text(self, marcel: Actor) -> None:
        """Can select an option from a dropdown by text."""
        test_text = "H"
        marcel.will(Open.their_browser_on(URL))
        marcel.will(
            Enter.the_text(test_text).into_the(ENTRY_INPUT),
            Wait.for_the(RESULT_TEXT).to_contain_text(test_text),
        )
        marcel.shall(
            See.the(Text.of_the(RESULT_TEXT), ReadsExactly(f"You entered: {test_text}"))
        )

    @act("Perform")
    @scene("Wait with custom")
    def test_wait_with_custom(self, marcel: Actor) -> None:
        """Can wait using a contrived custom wait function."""
        test_text = "H"

        def text_to_have_all(
            locator: Tuple[str, str], preamble: str, body: str, suffix: str
        ) -> Callable:
            """A very contrived custom condition."""

            def _predicate(driver: WebDriver) -> bool:
                element = driver.find_element(*locator)
                return f"{preamble} {body} {suffix}" in element.text

            return _predicate

        marcel.will(Open.their_browser_on(URL))
        marcel.will(
            Enter.the_text(test_text).into_the(ENTRY_INPUT),
            Wait()
            .using(text_to_have_all)
            .with_(RESULT_TEXT, "You", "entered:", test_text),
        )
        marcel.shall(
            See.the(Text.of_the(RESULT_TEXT), ReadsExactly(f"You entered: {test_text}"))
        )

