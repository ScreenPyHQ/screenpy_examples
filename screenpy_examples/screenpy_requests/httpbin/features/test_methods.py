"""
API test examples that use all the HTTP methods.
"""
from __future__ import annotations

import pytest
from screenpy import Actor, then, when
from screenpy.actions import See
from screenpy.resolutions import IsEqualTo, ReadsExactly
from screenpy_requests.actions import SendAPIRequest, SendGETRequest
from screenpy_requests.questions import (
    BodyOfTheLastResponse,
    StatusCodeOfTheLastResponse,
)

from screenpy_examples.screenpy_requests.httpbin.urls import BASE64_URL, BASE_URL


@pytest.mark.parametrize("action", ["DELETE", "GET", "PATCH", "POST", "PUT"])
def test_actions(action: str, Perry: Actor) -> None:
    """HTTP-action endpoints all respond with 200s."""
    when(Perry).attempts_to(SendAPIRequest(action, f"{BASE_URL}/{action.lower()}"))

    then(Perry).should(See.the(StatusCodeOfTheLastResponse(), IsEqualTo(200)))


def test_base64_decoder(Perry: Actor) -> None:
    """Base64 decoder correctly decodes string"""
    test_string = "QSBsb25nIHRpbWUgYWdvIGluIGEgZ2FsYXh5IGZhciwgZmFyIGF3YXk="

    when(Perry).attempts_to(SendGETRequest.to(f"{BASE64_URL}/{test_string}"))

    then(Perry).should(
        See.the(StatusCodeOfTheLastResponse(), IsEqualTo(200)),
        See.the(
            BodyOfTheLastResponse(),
            ReadsExactly("A long time ago in a galaxy far, far away"),
        ),
    )
