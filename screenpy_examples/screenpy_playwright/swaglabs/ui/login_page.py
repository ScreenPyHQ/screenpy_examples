from __future__ import annotations

from screenpy_playwright import Target

URL = "https://www.saucedemo.com/"

USERNAME_FIELD = Target.the("username field").located_by("#user-name")
PASSWORD_FIELD = Target.the("password field").located_by("#password")
LOGIN_BUTTON = Target.the('"Login" button').located_by("#login-button")
