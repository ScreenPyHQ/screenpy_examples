"""
Fixtures for the Android Appium example suite.
"""

from __future__ import annotations

import os
from typing import Generator

import pytest
from appium.webdriver import Remote
from screenpy import AnActor
from screenpy_appium.abilities import UseAnIOSDevice


@pytest.fixture(scope="function")
def Io() -> Generator:
    capabilities = {
        "app": os.path.abspath("../apps/ios-UICatalog.app.zip"),
        "automationName": "xcuitest",
        "deviceName": "iPhone Simulator",  # Appium will change to a specific device
        "newCommandTimeout": 10 * 1000,  # 10 seconds
        "platformName": "iOS",
        "platformVersion": "15.4",
        "simulatorStartupTimeout": 2 * 60 * 1000,  # 2 minutes
    }
    driver = Remote(
        command_executor="http://0.0.0.0:4723/wd/hub",
        desired_capabilities=capabilities,
    )

    the_actor = AnActor.named("Io").who_can(UseAnIOSDevice.using(driver))
    yield the_actor
    the_actor.exit()
