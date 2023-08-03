"""
API test example that tests various auths.
"""
from __future__ import annotations

from screenpy import Actor, IsEqualTo, See, given, then, when
from screenpy_requests.actions import AddHeader, SendGETRequest
from screenpy_requests.questions import StatusCodeOfTheLastResponse

from screenpy_examples.screenpy_requests.httpbin.urls import (
    BASIC_AUTH_URL,
    BEARER_AUTH_URL,
)


def test_basic_auth(Perry: Actor) -> None:
    """Basic authentication is accepted by the basic auth endpoint."""
    test_username = "USER"
    test_password = "PASS"

    when(Perry).attempts_to(
        SendGETRequest.to(f"{BASIC_AUTH_URL}/{test_username}/{test_password}").with_(
            auth=(test_username, test_password)
        )
    )

    then(Perry).should(See.the(StatusCodeOfTheLastResponse(), IsEqualTo(200)))


def test_bearer_auth(Perry: Actor) -> None:
    """Bearer token authentication is accepted by the bearer auth endpoint."""
    given(Perry).was_able_to(AddHeader(Authorization="Bearer 1234"))

    when(Perry).attempts_to(SendGETRequest.to(BEARER_AUTH_URL))

    then(Perry).should(See.the(StatusCodeOfTheLastResponse(), IsEqualTo(200)))
