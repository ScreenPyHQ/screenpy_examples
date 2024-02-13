"""
Fixtures for API testing.
"""

from __future__ import annotations

from typing import Generator

import pytest
from screenpy import AnActor, StdOutAdapter, StdOutManager, the_narrator
from screenpy_adapter_allure import AllureAdapter
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
