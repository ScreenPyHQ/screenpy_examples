"""
Our audience-polling mock-library for the example!

This library *purportedly* lets you to do polls on audiences. But it's a mock.
"""

from functools import wraps
from unittest import mock

import constants


tense_packet = mock.Mock()
tense_packet.top_mood = constants.TENSE
tense_packet.saturation = 90

laughter_packet = mock.Mock()
laughter_packet.top_mood = constants.LAUGHING
laughter_packet.saturation = 50

connect_to_audience = mock.Mock()


def mock_mood(packet):
    """This function allows tests to control how connect_to_audience is mocked."""

    def decorator_mock_mood(func):
        @wraps(func)
        def wrapper_func(*args, **kwargs):
            connect_to_audience().poll_mood.side_effect = [packet]
            func(*args, **kwargs)

        return wrapper_func

    return decorator_mock_mood
