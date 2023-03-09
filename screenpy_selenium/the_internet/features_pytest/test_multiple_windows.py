"""
An example of a test module that follows the typical unittest.TestCase
test structure. These tests exercise the SwitchToTab Action.
"""

from screenpy import Actor, given, then, when
from screenpy.actions import Pause, See
from screenpy.pacing import act, scene
from screenpy.resolutions import ContainsTheText, ReadsExactly
from screenpy_selenium.actions import Click, Open, SwitchToTab
from screenpy_selenium.questions import BrowserURL, Text

from ..user_interface.multiple_windows import (
    CLICK_HERE_LINK,
    HEADER_MESSAGE,
    URL,
)


class TestTabs:
    """
    Flexes the SwitchToTab Action.
    """

    @act("Perform")
    @scene("SwitchToTab")
    def test_switch_to_new_tab(self, marcel: Actor) -> None:
        """User is able to switch to a new tab."""
        marcel.will(Open.their_browser_on(URL))
        marcel.will(
            Click.on_the(CLICK_HERE_LINK),
            Pause.for_(1).second_because("Selenium needs to catch up"),
            SwitchToTab(2),
        )
        marcel.shall(
            See.the(BrowserURL(), ContainsTheText("windows/new")),
            See.the(Text.of_the(HEADER_MESSAGE), ReadsExactly("New Window")),
        )
