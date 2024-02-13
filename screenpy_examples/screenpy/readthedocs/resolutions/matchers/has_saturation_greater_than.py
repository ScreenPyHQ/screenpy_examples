# ruff: noqa: ANN401
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from hamcrest.core.base_matcher import BaseMatcher

if TYPE_CHECKING:
    from hamcrest.core.description import Description


class HasSaturationGreaterThan(BaseMatcher):
    """Assert that a mood object has at least a specific saturation level."""

    def _matches(self, item: Any) -> bool:
        """Whether the assertion passes."""
        return self.saturation_level <= item.saturation

    def describe_to(self, description: Description) -> None:
        """Describe the passing case."""
        description.append_text(
            f"the mood has a saturation level of at least {self.saturation_level}"
        )

    def describe_mismatch(self, item: Any, mismatch_description: Description) -> None:
        """Description used when a match fails."""
        mismatch_description.append_text(
            f"the saturation level was less than {self.saturation_level}"
        )

    def describe_match(self, item: Any, match_description: Description) -> None:
        """Description used when a negated match fails."""
        match_description.append_text(
            f"the saturation level was at least {self.saturation_level}"
        )

    def __init__(self, saturation_level: int) -> None:
        self.saturation_level = saturation_level


def is_palpable() -> HasSaturationGreaterThan:
    return HasSaturationGreaterThan(85)
