"""
The first screen of the application upon opening it.
"""

from __future__ import annotations

from screenpy_appium import Target

TEXT_FIELDS_BUTTON = Target.the('"Text Fields" button').located_by("Text Fields")
