"""
Setup and fixtures for our feature tests.
"""

from typing import Generator

import pytest
from screenpy import AnActor

from ..abilities import ControlCameras, PollTheAudience
from pollster import laughter_packet, tense_packet, connect_to_audience


@pytest.fixture
def Cameron() -> Generator:
    """Generate our cameraman, Cameron."""
    the_actor = AnActor.named("Cameron").who_can(ControlCameras())
    yield the_actor
    the_actor.exit()


@pytest.fixture
def Polly() -> Generator:
    """Generate our audience-polling stats wizard, Polly."""
    the_actor = AnActor.named("Polly").who_can(PollTheAudience())
    yield the_actor
    the_actor.exit()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_setup(item: pytest.Item) -> Generator:
    """This function makes the tests work in any order.

    You probably won't have this function in your tests for real, but we
    need to know which packet to load for our faked-out Pollster results.
    """
    side_effect = None
    if "comedic" in item.name:
        side_effect = laughter_packet
    elif "dramatic" in item.name:
        side_effect = tense_packet
    connect_to_audience().poll_mood.side_effect = [side_effect]
    yield
