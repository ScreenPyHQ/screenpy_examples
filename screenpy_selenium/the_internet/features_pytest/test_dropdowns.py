"""
An example of a test module that follows the typical unittest.TestCase
test structure. These tests exercise the selecting Actions.
"""
from screenpy import given, then, when
from screenpy.actions import See
from screenpy.pacing import act, scene
from screenpy.resolutions import ReadsExactly
from screenpy_selenium.actions import Open, Select
from screenpy_selenium.questions import Selected

from ..user_interface.dropdown import THE_DROPDOWN, URL


class TestDropdowns:
    """
    Flexes each selection strategy to select an option from a dropdown.
    """

    @act("Perform")
    @scene("Select by text")
    def test_select_by_text(self, marcel) -> None:
        """Can select an option from a dropdown by text."""
        marcel.will(Open.their_browser_on(URL))
        marcel.will(Select.the_option_named("Option 1").from_(THE_DROPDOWN))
        marcel.shall(
            See.the(Selected.option_from(THE_DROPDOWN), ReadsExactly("Option 1"))
        )

    @act("Perform")
    @scene("Select by index")
    def test_select_by_index(self, marcel) -> None:
        """Can select an option from a dropdown by index."""
        marcel.will(Open.their_browser_on(URL))
        marcel.will(Select.the_option_at_index(1).from_(THE_DROPDOWN))
        marcel.shall(
            See.the(Selected.option_from(THE_DROPDOWN), ReadsExactly("Option 1"))
        )

    @act("Perform")
    @scene("Select by value")
    def test_select_by_value(self, marcel) -> None:
        """Can select an option from a dropdown by value."""
        marcel.will(Open.their_browser_on(URL))
        marcel.will(Select.the_option_with_value("2").from_(THE_DROPDOWN))
        marcel.shall(
            See.the(Selected.option_from(THE_DROPDOWN), ReadsExactly("Option 2"))
        )

