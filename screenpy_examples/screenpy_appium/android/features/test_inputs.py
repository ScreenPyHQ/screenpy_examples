"""
Test interacting with inputs on Android.
"""


from screenpy import Actor, when, then
from screenpy.actions import Confirm, See
from screenpy.resolutions import ReadsExactly
from screenpy_appium.actions import Clear, Enter, Tap
from screenpy_appium.questions import Text

from ..ui.landing_screen import VIEWS_BUTTON
from ..ui.views_screen import TEXTFIELDS_BUTTON
from ..ui.text_fields_screen import TEXT_FIELDS


def test_enter_text(Andrew: Actor) -> None:
    test_text = "The larch."

    when(Andrew).attempts_to(
        Tap.on_the(VIEWS_BUTTON),
        Tap.on_the(TEXTFIELDS_BUTTON),
        Enter.the_text(test_text).into_the_first_of_the(TEXT_FIELDS),
    )

    then(Andrew).should(
        See.the(Text.of_the_first_of_the(TEXT_FIELDS), ReadsExactly(test_text))
    )


def test_clear_text(Andrew: Actor) -> None:
    test_text = "It is bereft of life!"

    when(Andrew).attempts_to(
        Tap.on_the(VIEWS_BUTTON),
        Tap.on_the(TEXTFIELDS_BUTTON),
        Enter.the_text(test_text).into_the_first_of_the(TEXT_FIELDS),
        Confirm.the(Text.of_the_first_of_the(TEXT_FIELDS), ReadsExactly(test_text)),
        Clear.the_text_from_the_first_of_the(TEXT_FIELDS),
    )

    then(Andrew).should(
        See.the(Text.of_the_first_of_the(TEXT_FIELDS), ReadsExactly("hint text"))
    )
