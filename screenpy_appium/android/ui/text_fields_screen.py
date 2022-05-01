"""
The screen that appears after tapping Text Fields in the Views screen.
"""

from screenpy_appium import Target


TEXT_FIELDS = Target.the("text fields").located_by("//android.widget.EditText")
