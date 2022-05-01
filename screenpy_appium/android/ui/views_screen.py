<<<<<<< HEAD
"""
The screen that appears after tapping Views on the landing page.
"""

=======
>>>>>>> 97e2d96c2cc38d10081c4efa593f141fbf697365
from screenpy_appium import Target

from .helpers import by_uiautomator_for


TEXTFIELDS_BUTTON = Target.the('"TextFields" button').located(
    by_uiautomator_for('description("TextFields")')
)
