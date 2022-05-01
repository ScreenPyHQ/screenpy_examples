from screenpy_appium import Target

from .helpers import by_uiautomator_for


TEXTFIELDS_BUTTON = Target.the('"TextFields" button').located(
    by_uiautomator_for('description("TextFields")')
)
