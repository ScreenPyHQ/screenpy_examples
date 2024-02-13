from __future__ import annotations

import os
from typing import TYPE_CHECKING, Generator, Type, TypeAlias

import pytest
from screenpy import (
    Actor,
    Forgettable,
    Performable,
    StdOutAdapter,
    StdOutManager,
    aside,
    the_narrator,
)
from setup_selenium import Browser, SetupSelenium, set_logger

from screenpy_examples.screenpy_logger import create_logger
from screenpy_selenium import BrowseTheWeb

if TYPE_CHECKING:
    from selenium.webdriver import Chrome, Edge, Firefox, Ie, Safari
    from selenium.webdriver.remote.webdriver import WebDriver
    from setup_selenium.selenium_module import T_DrvOpts

    AnyDriver: TypeAlias = Chrome | Firefox | Safari | Ie | Edge

logger = create_logger()
set_logger(logger)
the_narrator.adapters = [StdOutAdapter(StdOutManager(create_logger()))]


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
def selenium() -> Generator[WebDriver, None, None]:
    aside("Creating fixture Selenium Client FIXTURE")

    browser: Browser = Browser.CHROME
    headless: bool = True
    log_perf = False
    log_console = False
    log_driver = False
    log_dir = "./logs"
    driver_version: str | None = None
    browser_version: str | None = None
    binary_path: str | None = None
    driver_path: str | None = None

    if driver_path:
        driver_path = os.path.abspath(os.path.expanduser(driver_path))

    if binary_path:
        binary_path = os.path.abspath(os.path.expanduser(binary_path))

    driverpath, binarypath = SetupSelenium.install_driver(
        browser=browser,
        driver_version=driver_version,
        browser_version=browser_version,
        browser_path=binary_path,
    )
    driver_path = driver_path or driverpath
    binary_path = binary_path or binarypath
    aside(f"Using driver installed: {driver_path}")

    options: T_DrvOpts | None = None
    if browser == Browser.CHROME:
        options = SetupSelenium.chrome_options()
    elif browser == Browser.FIREFOX:
        options = SetupSelenium.firefox_options()
    elif browser == Browser.EDGE:
        options = SetupSelenium.edge_options()

    driver: AnyDriver = SetupSelenium.create_driver(
        browser=browser,
        headless=headless,
        enable_log_performance=log_perf,
        enable_log_console=log_console,
        enable_log_driver=log_driver,
        log_dir=log_dir,
        binary=binary_path,
        driver_path=driver_path,
        options=options,
    )
    driver.set_window_position(0, 0)
    driver.set_window_size(1600, 1080)
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
def marcel(selenium: WebDriver) -> Generator[Actor, None, None]:
    """A simple Actor fixture for the pytest example"""
    actor = Actor.named("Marcel").who_can(BrowseTheWeb.using(selenium))
    yield actor
    teardown_actor(actor)
