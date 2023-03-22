from __future__ import annotations
from typing import Any
from screenpy.pacing import beat
from hamcrest.core.base_matcher import Matcher


class IsEqualButRaisesException:
    """Resolution that raises an exception"""

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f"Equal to {self.expected}."

    @beat("... hoping it's equal to {expected}.")
    def resolve(self) -> Matcher[Any]:
        """Produce the Matcher to make the assertion."""
        raise Exception("This resolution raises exception")

    def __init__(self, obj: Any) -> None:
        self.expected = obj
