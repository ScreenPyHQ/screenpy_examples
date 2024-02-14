"""
An example of a test module that follows the typical unittest.TestCase
test structure. These tests exercise the selecting Actions.
"""

from __future__ import annotations

from screenpy import Actor, ReadsExactly, See, act, scene

from screenpy_examples.screenpy_selenium.the_internet.user_interface.dropdown import (
    THE_DROPDOWN,
    URL,
)
from screenpy_selenium import Open, Select, Selected


class TestDropdowns:
    """
    Flexes each selection strategy to select an option from a dropdown.
    """

    @act("Perform")
    @scene("Select by text")
    def test_select_by_text(self, marcel: Actor) -> None:
        """Can select an option from a dropdown by text."""
        marcel.will(Open.their_browser_on(URL))
        marcel.will(Select.the_option_named("Option 1").from_(THE_DROPDOWN))
        marcel.shall(
            See.the(Selected.option_from(THE_DROPDOWN), ReadsExactly("Option 1"))
        )

    @act("Perform")
    @scene("Select by index")
    def test_select_by_index(self, marcel: Actor) -> None:
        """Can select an option from a dropdown by index."""
        marcel.will(Open.their_browser_on(URL))
        marcel.will(Select.the_option_at_index(1).from_(THE_DROPDOWN))
        marcel.shall(
            See.the(Selected.option_from(THE_DROPDOWN), ReadsExactly("Option 1"))
        )

    @act("Perform")
    @scene("Select by value")
    def test_select_by_value(self, marcel: Actor) -> None:
        """Can select an option from a dropdown by value."""
        marcel.will(Open.their_browser_on(URL))
        marcel.will(Select.the_option_with_value("2").from_(THE_DROPDOWN))
        marcel.shall(
            See.the(Selected.option_from(THE_DROPDOWN), ReadsExactly("Option 2"))
        )
