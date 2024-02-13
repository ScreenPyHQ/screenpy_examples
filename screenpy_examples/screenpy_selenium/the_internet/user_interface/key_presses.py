"""
Locators and URL for the Key Presses page.
"""

from __future__ import annotations

from screenpy_selenium import Target

URL = "http://the-internet.herokuapp.com/key_presses"

ENTRY_INPUT = Target.the("entry input field").located_by("#target")
RESULT_TEXT = Target.the("result text").located_by("#result")
