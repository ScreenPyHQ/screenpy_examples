import pytest

from screenpy import AnActor
from screenpy.narration.adapters.stdout_adapter import StdOutAdapter, StdOutManager
from screenpy.pacing import the_narrator
from screenpy_playwright.abilities import BrowseTheWebSynchronously

from screenpy_examples.screenpy_playwright.swaglabs.screenpy_logger import create_logger

the_narrator.adapters = [StdOutAdapter(StdOutManager(create_logger("scr")))]


@pytest.fixture(scope="function")
def Swalter() -> AnActor:
    """Swalter tests Swaglabs."""
    the_actor = AnActor.named("Swalter").who_can(
        BrowseTheWebSynchronously.using_firefox()
    )
    yield the_actor
    the_actor.exit()
