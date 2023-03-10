"""
Setup and fixtures for our feature tests.
"""

import logging
from typing import Generator

import _pytest.logging
import pytest

from screenpy import AnActor
from screenpy.narration.adapters.stdout_adapter import StdOutAdapter, StdOutManager
from screenpy.pacing import the_narrator

from screenpy_examples.screenpy.readthedocs.abilities import (
    ControlCameras,
    PollTheAudience,
)
from screenpy_examples.screenpy.readthedocs.pollster import (
    connect_to_audience,
    laughter_packet,
    tense_packet,
)
from screenpy_examples.screenpy_logger import create_logger

the_narrator.adapters = [StdOutAdapter(StdOutManager(create_logger()))]


@pytest.fixture
def Cameron() -> Generator:
    """Generate our cameraman, Cameron."""
    the_actor = AnActor.named("Cameron").who_can(ControlCameras())
    yield the_actor
    the_actor.exit()


@pytest.fixture
def Polly() -> Generator:
    """Generate our audience-polling stats wizard, Polly."""
    the_actor = AnActor.named("Polly").who_can(PollTheAudience())
    yield the_actor
    the_actor.exit()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_setup(item: pytest.Item) -> Generator:
    """This function makes the tests work in any order.

    You probably won't have this function in your tests for real, but we
    need to know which packet to load for our faked-out Pollster results.
    """
    side_effect = None
    if "comedic" in item.name:
        side_effect = laughter_packet
    elif "dramatic" in item.name:
        side_effect = tense_packet
    connect_to_audience().poll_mood.side_effect = [side_effect]
    yield


@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    logging_plugin = config.pluginmanager.get_plugin("logging-plugin")
    formatter = logging_plugin.log_cli_handler.formatter

    if isinstance(formatter, _pytest.logging.ColoredLevelFormatter):
        formatter.add_color_level(logging.INFO, "green")
        formatter.add_color_level(logging.ERROR, "red")
    return
