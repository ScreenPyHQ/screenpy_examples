"""
An example of a test module that follows the typical unittest.TestCase
test structure. These tests exercise the frame switching Actions.
"""
from __future__ import annotations

import unittest

from screenpy import AnActor, given, then, when
from screenpy.actions import See
from screenpy.pacing import act, scene
from screenpy.resolutions import ReadsExactly
from screenpy_selenium.abilities import BrowseTheWeb
from screenpy_selenium.actions import Open, SwitchTo
from screenpy_selenium.questions import Text

from screenpy_examples.screenpy_selenium.the_internet.user_interface.iframe import (
    CONTENT_BOX,
    URL,
    WYSIWYG_IFRAME,
)


class TestFrames(unittest.TestCase):
    """
    Flexes the SwitchTo Action.
    """

    def setUp(self) -> None:
        self.actor = AnActor.named("Perry").who_can(BrowseTheWeb.using_firefox())

    @act("Perform")
    @scene("SwitchTo")
    def test_switch_to_iframe(self) -> None:
        """User is able to switch to an iframe."""
        Perry = self.actor

        given(Perry).was_able_to(Open.their_browser_on(URL))
        when(Perry).attempts_to(SwitchTo.the(WYSIWYG_IFRAME))
        then(Perry).should(
            See.the(Text.of_the(CONTENT_BOX), ReadsExactly("Your content goes here."))
        )

    def tearDown(self) -> None:
        self.actor.exit()
