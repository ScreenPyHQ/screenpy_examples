"""
Our audience-polling mock-library for the example!

This library *purportedly* lets you to do polls on audiences. But it's a mock.
"""
from __future__ import annotations

from unittest import mock

from screenpy_examples.screenpy.readthedocs import constants

tense_packet = mock.Mock()
tense_packet.top_mood = constants.TENSE
tense_packet.saturation = 90

laughter_packet = mock.Mock()
laughter_packet.top_mood = constants.LAUGHING
laughter_packet.saturation = 50

connect_to_audience = mock.Mock()
