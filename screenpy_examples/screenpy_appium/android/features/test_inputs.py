"""
Test interacting with inputs on Android.
"""

from __future__ import annotations

from screenpy import Actor, Confirm, ReadsExactly, See, then, when
from screenpy_appium.actions import Clear, Enter, Tap
from screenpy_appium.questions import Text

from screenpy_examples.screenpy_appium.android.ui.landing_screen import VIEWS_BUTTON
from screenpy_examples.screenpy_appium.android.ui.text_fields_screen import TEXT_FIELDS
from screenpy_examples.screenpy_appium.android.ui.views_screen import TEXTFIELDS_BUTTON


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
