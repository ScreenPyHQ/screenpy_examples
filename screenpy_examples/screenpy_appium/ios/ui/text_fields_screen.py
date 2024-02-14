"""
The screen that appears after tapping "Text Fields".
"""

from __future__ import annotations

from screenpy_appium import Target

TEXT_FIELDS = Target.the("text fields").located_by("//XCUIElementTypeTextField")
