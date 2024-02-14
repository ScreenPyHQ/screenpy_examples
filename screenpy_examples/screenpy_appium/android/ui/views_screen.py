"""
The screen that appears after tapping Views on the landing page.
"""

from __future__ import annotations

from screenpy_appium import Target

from screenpy_examples.screenpy_appium.android.ui.helpers import by_uiautomator_for

TEXTFIELDS_BUTTON = Target.the('"TextFields" button').located(
    by_uiautomator_for('description("TextFields")')
)
