"""
An example of a test module that follows the typical unittest.TestCase
test structure. These tests exercise the clicking and waiting Actions.
"""
from __future__ import annotations

import random

from screenpy.actions import See
from screenpy.pacing import act, scene
from screenpy.resolutions import ContainsTheText, IsEqualTo
from screenpy_selenium.actions import Click, Open, Wait
from screenpy_selenium.questions import Attribute, Element, Number
from screenpy_selenium.resolutions import IsVisible

from ..user_interface.add_remove_elements import ADD_BUTTON, ADDED_ELEMENTS, URL


class TestAddRemoveElements:
    """
    Flexes the Add and Remove Elements page of http://the-internet.herokuapp.com/
    """

    @act("Perform")
    @scene("Click")
    def test_add_one_element(self, marcel) -> None:
        """User is able to add one element."""
        marcel.will(Open.their_browser_on(URL))
        marcel.will(Click.on_the(ADD_BUTTON), Wait.for_the(ADDED_ELEMENTS))
        marcel.shall(See.the(Element(ADDED_ELEMENTS), IsVisible()))

    @act("Perform")
    @scene("Click")
    def test_add_many_elements(self, marcel) -> None:
        """
        User is able to add many elements. This test chooses a random
        number of elements to add, just to show off how to do that, if you
        want to do something like that.
        """
        number_of_times = random.choice(range(2, 10))

        marcel.will(Open.their_browser_on(URL))
        marcel.will(*(Click.on_the(ADD_BUTTON) for each_time in range(number_of_times)))
        marcel.shall(See.the(Number.of(ADDED_ELEMENTS), IsEqualTo(number_of_times)))

    @act("Perform")
    @scene("Click")
    def test_remove_element(self, marcel) -> None:
        """User is able to remove an element that was added."""
        marcel.will(
            Open.their_browser_on(URL),
            Click.on_the(ADD_BUTTON),
            Wait.for_the(ADDED_ELEMENTS),
        )
        marcel.will(Click.on_the(ADDED_ELEMENTS))
        marcel.shall(See.the(Number.of(ADDED_ELEMENTS), IsEqualTo(0)))

    @act("Perform")
    @scene("Attribute")
    def test_class_name(self, marcel) -> None:
        """Class name is correctly set."""
        marcel.will(
            Open.their_browser_on(URL),
            Click.on_the(ADD_BUTTON),
            Wait.for_the(ADDED_ELEMENTS),
        )
        marcel.shall(
            See.the(
                Attribute("class").of_the(ADDED_ELEMENTS),
                ContainsTheText("added-manually"),
            ),
        )

    @act("Perform")
    @scene("Attribute")
    def test_many_class_names(self, marcel) -> None:
        """Class name is correctly set."""
        number_of_times = random.choice(range(2, 10))

        marcel.will(
            Open.their_browser_on(URL),
            *(Click.on_the(ADD_BUTTON) for each_time in range(number_of_times)),
            Wait.for_the(ADDED_ELEMENTS),
        )
        marcel.shall(
            See.the(
                Attribute("class").of_all(ADDED_ELEMENTS),
                IsEqualTo(["added-manually"] * number_of_times),
            ),
        )
