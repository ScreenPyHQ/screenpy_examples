"""
Test interacting with inputs on iOS.
"""

from screenpy import Actor, when, then
from screenpy.actions import Confirm, See
from screenpy.resolutions import ReadsExactly
from screenpy_appium.actions import Clear, Enter, Tap
from screenpy_appium.questions import Text

from ui.landing_screen import TEXT_FIELDS_BUTTON
from ui.text_fields_screen import TEXT_FIELDS


def test_enter_text(Io: Actor) -> None:
    test_text = "I've come for an argument."

    when(Io).attempts_to(
        Tap.on_the(TEXT_FIELDS_BUTTON),
        Enter.the_text(test_text).into_the_first_of_the(TEXT_FIELDS),
    )

    then(Io).should(
        See.the(Text.of_the_first_of_the(TEXT_FIELDS), ReadsExactly(test_text))
    )


def test_clear_text(Io: Actor) -> None:
    test_text = "Nod's as good as a wink to a blind bat, eh?"

    when(Io).attempts_to(
        Tap.on_the(TEXT_FIELDS_BUTTON),
        Enter.the_text(test_text).into_the_first_of_the(TEXT_FIELDS),
        Confirm.the(Text.of_the_first_of_the(TEXT_FIELDS), ReadsExactly(test_text)),
        Clear.the_text_from_the_first_of_the(TEXT_FIELDS),
    )

    then(Io).should(
        See.the(Text.of_the_first_of_the(TEXT_FIELDS), ReadsExactly("Placeholder text"))
    )
