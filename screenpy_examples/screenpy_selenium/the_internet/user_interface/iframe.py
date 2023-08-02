"""
Locators and URL for the Iframe page.
"""
from __future__ import annotations

from screenpy_selenium import Target

URL = "http://the-internet.herokuapp.com/iframe"

WYSIWYG_IFRAME = Target.the("WYSIWYG iframe").located_by("#mce_0_ifr")
CONTENT_BOX = Target.the("content box").located_by("p")
