from screenpy import Actor
from screenpy_playwright.actions import Click, Enter, Visit

from screenpy_examples.screenpy_playwright.swaglabs.ui.login_page import (
    LOGIN_BUTTON,
    PASSWORD_FIELD,
    URL,
    USERNAME_FIELD,
)
from screenpy_examples.screenpy_playwright.swaglabs.user_types import User


class LogIn:
    """Log in with the supplied user or username/password combination.

    Examples::

        the_actor.attempts_to(LogIn.as_(StandardUser))

        the_actor.attempts_to(LogIn.using("username", "password"))
    """

    @staticmethod
    def as_(user: User) -> "LogIn":
        """Log in as a predefined user."""
        return LogIn.using(user.username, user.password)

    @staticmethod
    def using(username: str, password: str) -> "LogIn":
        """Log in using the supplied username and password combination."""
        return LogIn(username, password)

    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to log in."""
        the_actor.attempts_to(
            Visit(URL),
            Enter.the_text(self.username).into_the(USERNAME_FIELD),
            Enter.the_password(self.password).into_the(PASSWORD_FIELD),
            Click.on_the(LOGIN_BUTTON),
        )

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
