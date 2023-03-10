"""
Fixtures for API testing.
"""

from typing import Generator

import pytest
from screenpy_adapter_allure import AllureAdapter

from screenpy import AnActor
from screenpy.narration.adapters.stdout_adapter import StdOutAdapter, StdOutManager
from screenpy.pacing import the_narrator
from screenpy_requests.abilities import MakeAPIRequests

from screenpy_examples.screenpy_logger import create_logger

the_narrator.adapters.append(AllureAdapter())

the_narrator.adapters = [StdOutAdapter(StdOutManager(create_logger()))]


@pytest.fixture
def Perry() -> Generator:
    """An Actor who can make API requests."""
    the_actor = AnActor.named("Perry").who_can(MakeAPIRequests())
    yield the_actor
    the_actor.exit_stage_left()
