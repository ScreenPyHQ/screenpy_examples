"""
An example of a test module that follows the typical unittest.TestCase
test structure. These tests exercise the frame switching Actions.
"""
from screenpy.actions import Eventually, See
from screenpy.pacing import act, scene
from screenpy.resolutions import ReadsExactly
from screenpy_selenium.actions import Open, SwitchTo
from screenpy_selenium.questions import Text

from screenpy_examples.screenpy_selenium.the_internet.user_interface.iframe import (
    CONTENT_BOX,
    URL,
    WYSIWYG_IFRAME,
)


class TestFrames:
    """
    Flexes the SwitchTo Action.
    """

    @act("Perform")
    @scene("SwitchTo")
    def test_switch_to_iframe(self, marcel) -> None:
        """User is able to switch to an iframe."""
        marcel.will(Open.their_browser_on(URL))
        marcel.will(SwitchTo.the(WYSIWYG_IFRAME))
        marcel.shall(
            Eventually(
                See.the(
                    Text.of_the(CONTENT_BOX), ReadsExactly("Your content goes here.")
                )
            )
        )
