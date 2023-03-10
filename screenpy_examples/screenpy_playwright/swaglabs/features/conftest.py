from typing import Generator

import pytest

from screenpy import AnActor
from screenpy_playwright.abilities import BrowseTheWebSynchronously
from screenpy.pacing import the_narrator
from ..screenpy_logger import create_logger
from screenpy.narration.adapters.stdout_adapter import StdOutAdapter, StdOutManager

the_narrator.adapters = [StdOutAdapter(StdOutManager(create_logger("scr")))]


@pytest.fixture(scope="function")
def Swalter() -> AnActor:
    """Swalter tests Swaglabs."""
    the_actor = AnActor.named("Swalter").who_can(
        BrowseTheWebSynchronously.using_firefox()
    )
    yield the_actor
    the_actor.exit()
