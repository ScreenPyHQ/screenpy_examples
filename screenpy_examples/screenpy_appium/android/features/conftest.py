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
def Andrew() -> Generator:
    capabilities = {
        "app": os.path.abspath("../apps/android-ApiDemos-debug.apk.zip"),
        "platformName": "Android",
        "deviceName": "ScreenPy",
        "newCommandTimeout": 4 * 60,  # 4 minutes
        "automationName": "UIAutomator2",
        "uiautomator2ServerInstallTimeout": 2 * 60 * 1000,  # 2 minutes
        "adbExecTimeout": 2 * 60 * 1000,  # 2 minutes
    }
    driver = Remote(
        command_executor="http://0.0.0.0:4723/wd/hub",
        desired_capabilities=capabilities,
    )

    the_actor = AnActor.named("Andrew").who_can(UseAnIOSDevice.using(driver))
    yield the_actor
    the_actor.exit()
