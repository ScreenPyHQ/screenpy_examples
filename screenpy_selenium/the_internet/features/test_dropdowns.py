"""
An example of a test module that follows the typical unittest.TestCase
test structure. These tests exercise the selecting Actions.
"""

import unittest

from selenium.webdriver import Firefox

from screenpy import AnActor, given, then, when
from screenpy.actions import See
from screenpy.pacing import act, scene
from screenpy.resolutions import ReadsExactly
from screenpy_selenium.abilities import BrowseTheWeb
from screenpy_selenium.actions import Open, Select
from screenpy_selenium.questions import Selected

from the_internet.user_interface.dropdown import THE_DROPDOWN, URL


class TestDropdowns(unittest.TestCase):
    """
    Flexes each selection strategy to select an option from a dropdown.
    """

    def setUp(self) -> None:
        self.actor = AnActor.named("Perry").who_can(BrowseTheWeb.using(Firefox()))

    @act("Perform")
    @scene("Select by text")
    def test_select_by_text(self) -> None:
        """Can select an option from a dropdown by text."""
        Perry = self.actor

        given(Perry).was_able_to(Open.their_browser_on(URL))
        when(Perry).attempts_to(Select.the_option_named("Option 1").from_(THE_DROPDOWN))
        then(Perry).should(
            See.the(Selected.option_from(THE_DROPDOWN), ReadsExactly("Option 1"))
        )

    @act("Perform")
    @scene("Select by index")
    def test_select_by_index(self) -> None:
        """Can select an option from a dropdown by index."""
        Perry = self.actor

        given(Perry).was_able_to(Open.their_browser_on(URL))
        when(Perry).attempts_to(Select.the_option_at_index(1).from_(THE_DROPDOWN))
        then(Perry).should(
            See.the(Selected.option_from(THE_DROPDOWN), ReadsExactly("Option 1"))
        )

    @act("Perform")
    @scene("Select by value")
    def test_select_by_value(self) -> None:
        """Can select an option from a dropdown by value."""
        Perry = self.actor

        given(Perry).was_able_to(Open.their_browser_on(URL))
        when(Perry).attempts_to(Select.the_option_with_value("2").from_(THE_DROPDOWN))
        then(Perry).should(
            See.the(Selected.option_from(THE_DROPDOWN), ReadsExactly("Option 2"))
        )

    def tearDown(self) -> None:
        self.actor.exit_stage_right()
