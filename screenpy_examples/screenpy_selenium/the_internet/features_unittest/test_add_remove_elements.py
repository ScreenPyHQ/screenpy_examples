"""
An example of a test module that follows the typical unittest.TestCase
test structure. These tests exercise the clicking and waiting Actions.
"""

from __future__ import annotations

import random
import unittest

from screenpy import (
    AnActor,
    ContainsTheText,
    IsEqualTo,
    See,
    act,
    given,
    scene,
    then,
    when,
)
from selenium.webdriver import Firefox

from screenpy_selenium import (
    Attribute,
    BrowseTheWeb,
    Click,
    Element,
    IsVisible,
    Number,
    Open,
    Wait,
)

from ..user_interface.add_remove_elements import ADD_BUTTON, ADDED_ELEMENTS, URL


class TestAddRemoveElements(unittest.TestCase):
    """
    Flexes the Add and Remove Elements page of http://the-internet.herokuapp.com/
    """

    def setUp(self) -> None:
        self.actor = AnActor.named("Oona").who_can(BrowseTheWeb.using(Firefox()))

    def tearDown(self) -> None:
        self.actor.exit_stage_left()

    @act("Perform")
    @scene("Click")
    def test_add_one_element(self) -> None:
        """User is able to add one element."""
        Oona = self.actor

        given(Oona).was_able_to(Open.their_browser_on(URL))
        when(Oona).attempts_to(Click.on_the(ADD_BUTTON), Wait.for_the(ADDED_ELEMENTS))
        then(Oona).should(See.the(Element(ADDED_ELEMENTS), IsVisible()))

    @act("Perform")
    @scene("Click")
    def test_add_many_elements(self) -> None:
        """
        User is able to add many elements. This test chooses a random
        number of elements to add, just to show off how to do that, if you
        want to do something like that.
        """
        Oona = self.actor
        number_of_times = random.choice(range(2, 10))

        given(Oona).was_able_to(Open.their_browser_on(URL))
        when(Oona).attempts_to(
            *(Click.on_the(ADD_BUTTON) for each_time in range(number_of_times))
        )
        then(Oona).should(
            See.the(Number.of(ADDED_ELEMENTS), IsEqualTo(number_of_times))
        )

    @act("Perform")
    @scene("Click")
    def test_remove_element(self) -> None:
        """User is able to remove an element that was added."""
        Oona = self.actor

        given(Oona).was_able_to(
            Open.their_browser_on(URL),
            Click.on_the(ADD_BUTTON),
            Wait.for_the(ADDED_ELEMENTS),
        )
        when(Oona).attempts_to(Click.on_the(ADDED_ELEMENTS))
        then(Oona).should(See.the(Number.of(ADDED_ELEMENTS), IsEqualTo(0)))

    @act("Perform")
    @scene("Attribute")
    def test_class_name(self) -> None:
        """Class name is correctly set."""
        Oona = self.actor

        given(Oona).was_able_to(
            Open.their_browser_on(URL),
            Click.on_the(ADD_BUTTON),
            Wait.for_the(ADDED_ELEMENTS),
        )
        then(Oona).should(
            See.the(
                Attribute("class").of_the(ADDED_ELEMENTS),
                ContainsTheText("added-manually"),
            ),
        )

    @act("Perform")
    @scene("Attribute")
    def test_many_class_names(self) -> None:
        """Class name is correctly set."""
        Oona = self.actor
        number_of_times = random.choice(range(2, 10))

        given(Oona).was_able_to(
            Open.their_browser_on(URL),
            *(Click.on_the(ADD_BUTTON) for each_time in range(number_of_times)),
            Wait.for_the(ADDED_ELEMENTS),
        )
        then(Oona).should(
            See.the(
                Attribute("class").of_all(ADDED_ELEMENTS),
                IsEqualTo(["added-manually"] * number_of_times),
            ),
        )
