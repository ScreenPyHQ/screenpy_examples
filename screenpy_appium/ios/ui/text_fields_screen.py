"""
The screen that appears after tapping "Text Fields".
"""

from screenpy_appium import Target


TEXT_FIELDS = Target.the("text fields").located_by("//XCUIElementTypeTextField")
