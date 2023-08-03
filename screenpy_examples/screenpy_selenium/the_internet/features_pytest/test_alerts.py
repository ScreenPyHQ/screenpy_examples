"""
An example of a test module that follows the typical unittest.TestCase
test structure. These tests exercise the alert checking Actions.
"""
from __future__ import annotations

from screenpy import ReadsExactly, See, act, scene
from screenpy_selenium import (
    AcceptAlert,
    Click,
    DismissAlert,
    Open,
    RespondToPrompt,
    Text,
    TextOfTheAlert,
)

from screenpy_examples.screenpy_selenium.the_internet.actions import TryTo

from ..user_interface.javascript_alerts import (
    JS_ALERT_BUTTON,
    JS_CONFIRM_BUTTON,
    JS_PROMPT_BUTTON,
    RESULT_MESSAGE,
    URL,
)


class TestAlerts:
    """
    Flexes the AcceptAlert, DismissAlert, and RespondToPrompt Actions, as
    well as the TextOfTheAlert Question.
    """

    @act("Perform")
    @scene("TextOfTheAlert")
    def test_inspect_alert(self, marcel) -> None:
        """User can read the text of the alert."""
        marcel.will(Open.their_browser_on(URL))
        marcel.will(Click.on_the(JS_ALERT_BUTTON))
        marcel.shall(See.the(TextOfTheAlert(), ReadsExactly("I am a JS Alert")))

    @act("Perform")
    @scene("AcceptAlert")
    def test_accept_alert(self, marcel) -> None:
        """User can accept an alert."""
        marcel.will(
            TryTo(
                See.the(TextOfTheAlert(), ReadsExactly("I am a JS Alert")),
                AcceptAlert(),
            ).otherwise(Open.their_browser_on(URL))
        )
        marcel.will(TryTo(Click.on_the(JS_CONFIRM_BUTTON)))
        marcel.will(AcceptAlert())
        marcel.shall(
            See.the(Text.of_the(RESULT_MESSAGE), ReadsExactly("You clicked: Ok"))
        )

    @act("Perform")
    @scene("DismissAlert")
    def test_dismiss_alert(self, marcel) -> None:
        """User can dismiss an alert."""
        marcel.will(Open.their_browser_on(URL), Click.on_the(JS_CONFIRM_BUTTON))
        marcel.will(DismissAlert())
        marcel.shall(
            See.the(Text.of_the(RESULT_MESSAGE), ReadsExactly("You clicked: Cancel"))
        )

    @act("Perform")
    @scene("RespondToPrompt")
    def test_respond_to_prompt(self, marcel) -> None:
        """User can enter text into a prompt."""
        test_text = "Hello! I am responding to this prompt."

        marcel.will(Open.their_browser_on(URL), Click.on_the(JS_PROMPT_BUTTON))
        marcel.will(RespondToPrompt.with_(test_text))
        marcel.shall(
            See.the(
                Text.of_the(RESULT_MESSAGE), ReadsExactly(f"You entered: {test_text}")
            )
        )
