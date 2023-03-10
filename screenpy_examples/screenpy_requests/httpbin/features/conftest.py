"""
Fixtures for API testing.
"""

from typing import Generator

import pytest
from screenpy_adapter_allure import AllureAdapter

from screenpy import AnActor
from screenpy.pacing import the_narrator
from screenpy_requests.abilities import MakeAPIRequests

the_narrator.adapters.append(AllureAdapter())


@pytest.fixture
def Perry() -> Generator:
    """An Actor who can make API requests."""
    the_actor = AnActor.named("Perry").who_can(MakeAPIRequests())
    yield the_actor
    the_actor.exit_stage_left()
