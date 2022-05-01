"""
The first screen of the application upon opening it.
"""

from screenpy_appium import Target

from .helpers import by_uiautomator_for


VIEWS_BUTTON = Target.the('"Views" button').located(
    by_uiautomator_for('description("Views")')
)
