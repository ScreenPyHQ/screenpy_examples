"""
Setup and fixtures for our feature tests.
"""

from typing import Generator

import pytest
from screenpy import AnActor

from ..abilities import ControlCameras, PollTheAudience


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
