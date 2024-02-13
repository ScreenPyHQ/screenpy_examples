"""
Our camera-controlling mock-library for the example!

This library *purportedly* allows you to control cameras. But it's a mock.
"""

from __future__ import annotations

from unittest import mock


def Camera(character: str) -> mock.MagicMock:
    return mock.MagicMock(character=character)


RecordingSession = mock.MagicMock()
