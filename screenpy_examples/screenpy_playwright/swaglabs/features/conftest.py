from __future__ import annotations

from typing import Any, Generator

import pytest
from screenpy import AnActor, StdOutAdapter, StdOutManager, the_narrator
from screenpy_playwright.abilities import BrowseTheWebSynchronously

from screenpy_examples.screenpy_logger import create_logger

the_narrator.adapters = [StdOutAdapter(StdOutManager(create_logger()))]


@pytest.fixture(scope="function")
def Swalter() -> Generator[AnActor, Any, None]:
    """Swalter tests Swaglabs."""
    the_actor = AnActor.named("Swalter").who_can(
        BrowseTheWebSynchronously.using_firefox()
    )
    yield the_actor
    the_actor.exit()
