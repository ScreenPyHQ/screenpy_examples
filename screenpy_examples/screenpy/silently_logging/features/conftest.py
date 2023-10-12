from __future__ import annotations

from typing import Generator

import pytest
from screenpy import Actor, StdOutAdapter, StdOutManager, aside, settings, the_narrator

from screenpy_examples.screenpy_logger import create_logger

logger = create_logger()
the_narrator.adapters = [StdOutAdapter(StdOutManager(create_logger()))]


settings.TIMEOUT = 2
settings.POLLING = 0.1


def teardown_actor(actor: Actor):
    aside(f"{actor} exits stage left!")
    actor.exit_stage_left()


@pytest.fixture(scope="session")
def marcel() -> Generator[Actor, None, None]:
    """A simple Actor fixture for the pytest example"""
    actor = Actor.named("Marcel").who_can()
    yield actor
    teardown_actor(actor)
