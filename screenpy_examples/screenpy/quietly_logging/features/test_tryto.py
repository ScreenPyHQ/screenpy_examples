from __future__ import annotations

import pytest

from screenpy import Actor

from screenpy_examples.screenpy.quietly_logging.actions import (
    DoA,
    DoB,
    DoChatty,
    DoChattyFail,
    DoFail,
    DoFailCounter,
    DoFirst,
    DoPass,
    DoPassAfterAWhile,
    DoSecond,
    Quietly,
    TryTo,
)


def test_first_action_pass(marcel: Actor) -> None:
    """
    Demonstrates logging of a TryTo:
        perform first action which passes
        and not perform the second action

    Marcel tries to DoFirst
        Marcel tries to DoPass
            Marcel sees if simpleQuestion is equal to True.
    """
    marcel.will(TryTo(DoFirst()).otherwise(DoSecond()))


def test_first_action_fail(marcel: Actor) -> None:
    """
    Demonstrates logging of a TryTo:
        perform first action which fails
        and then perform second action which passes

    Marcel tries to DoSecond
        Marcel tries to DoPass
            Marcel sees if simpleQuestion is equal to True.
    """
    marcel.will(TryTo(DoFirst(DoFail())).otherwise(DoSecond()))


def test_first_and_second_action_fail(marcel: Actor) -> None:
    """
    Demonstrates logging of a TryTo:
        perform the first action which fails
        and perform second action which fails

    Marcel tries to DoSecond
        Marcel tries to DoFail
            Marcel sees if simpleQuestion is equal to False.
                Marcel examines SimpleQuestion
                    => True
                ... hoping it's equal to False.
                    => <False>
    ***ERROR***

    AssertionError: 
    Expected: <False>
         but: was <True>
    """
    marcel.will(TryTo(DoFirst(DoFail())).otherwise(DoSecond(DoFail())))
