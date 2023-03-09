from __future__ import annotations
from typing import TYPE_CHECKING, Generator, Type

import pytest
from screenpy import aside, Actor
from screenpy.narration.adapters.stdout_adapter import StdOutAdapter, StdOutManager
from screenpy.pacing import the_narrator
from screenpy.protocols import Forgettable, Performable
from screenpy_selenium.abilities import BrowseTheWeb
from screenpy import settings
from ..screenpy_logger import create_logger
from .setup_selenium import Selenium

if TYPE_CHECKING:
    # from _pytest.config import Config
    # from _pytest.config.argparsing import Parser
    from _pytest.fixtures import SubRequest
    from selenium.webdriver.remote.webdriver import WebDriver

the_narrator.adapters = [StdOutAdapter(StdOutManager(create_logger("nxt")))]


class RemoveAbilityWithouClosingSelenium(Performable):
    """
    Actors already have a method to remove an ability, but in some cases
    we do not want ability.forget() to be called.
    """

    def perform_as(self, actor: Actor) -> None:
        actor.abilities.remove(actor.uses_ability_to(self.ability))

    def __init__(self, ability: Type[Forgettable]):
        self.ability = ability


@pytest.fixture(scope="session", autouse=True)
def selenium(request: "SubRequest") -> Generator["WebDriver", None, None]:
    aside("Creating fixture Selenium Client FIXTURE")
    settings.TIMEOUT = 6
    browser = "chrome"
    headless = False
    log_perf = False 
    log_console = False
    log_driver = False
    log_path = "./logs"
    driver_version = "auto"

    driver = Selenium.create_driver(
        browser=browser,
        headless=headless,
        enable_log_performance=log_perf,
        enable_log_console=log_console,
        enable_log_driver=log_driver,
        log_path=log_path,
        version=driver_version,
    )
    driver.set_window_size(1280, 960)
    driver.set_window_position(0, 0)
    aside("Creating Selenium Client FIXTURE - Complete")
    yield driver
    aside("closing selenium FIXTURE")
    if driver:
        driver.quit()


def teardown_actor(actor: Actor):
    aside(f"{actor} exits stage left!")
    actor.will(RemoveAbilityWithouClosingSelenium(BrowseTheWeb))
    actor.exit_stage_left()


@pytest.fixture(scope="session")
def Oona(selenium: WebDriver) -> Generator[Actor, None, None]:
    """A simple Actor fixture for the pytest example"""
    actor = Actor.named("Oona").who_can(BrowseTheWeb.using(selenium))
    yield actor
    teardown_actor(actor)


@pytest.fixture(scope="session")
def marcel(selenium: WebDriver) -> Generator[Actor, None, None]:
    """A simple Actor fixture for the pytest example"""
    actor = Actor.named("Marcel").who_can(BrowseTheWeb.using(selenium))
    yield actor
    teardown_actor(actor)
