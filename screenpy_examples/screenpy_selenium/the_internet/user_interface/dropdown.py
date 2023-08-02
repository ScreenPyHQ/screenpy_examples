"""
Locators and URL for the Dropdown page.
"""
from __future__ import annotations

from screenpy_selenium import Target

URL = "http://the-internet.herokuapp.com/dropdown"

THE_DROPDOWN = Target.the("dropdown menu").located_by("#dropdown")
