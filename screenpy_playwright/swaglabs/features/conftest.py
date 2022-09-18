from typing import Generator

import pytest

from screenpy import AnActor
from screenpy_playwright.abilities import BrowseTheWebSynchronously


@pytest.fixture(scope="function")
def Swalter() -> Generator:
    """Swalter tests Swaglabs."""
    the_actor = AnActor.named("Swalter").who_can(
        BrowseTheWebSynchronously.using_firefox()
    )
    yield the_actor
    the_actor.exit()
