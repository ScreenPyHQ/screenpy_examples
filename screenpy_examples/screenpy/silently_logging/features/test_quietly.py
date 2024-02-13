from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy import Eventually, IsEqual, Quietly

from screenpy_examples.screenpy.silently_logging.actions import (
    PerformA,
    PerformB,
    PerformChatty,
    PerformChattyFail,
    PerformFail,
    PerformFailCounter,
    PerformPass,
    PerformPassAfterAWhile,
    See,
)
from screenpy_examples.screenpy.silently_logging.questions import (
    SimpleQuestion,
    SimpleQuestionException,
)
from screenpy_examples.screenpy.silently_logging.resolutions import (
    IsEqualButRaisesException,
)

if TYPE_CHECKING:
    from screenpy import Actor


def test_eventually_succeeds(marcel: Actor) -> None:
    marcel.will(Eventually(PerformPassAfterAWhile()).for_(1).seconds())


def test_eventually_fails(marcel: Actor) -> None:
    marcel.will(Eventually(PerformFailCounter()).for_(1).seconds())


## TODO: remove this comment after pr is merged
## all of the exmaples below are using the refactor-resolutions branch
## https://github.com/ScreenPyHQ/screenpy/pull/57


def test_passes_without_quietly(marcel: Actor) -> None:
    """
    Generates a normal log:

    Marcel tries to PerformChatty
        Marcel tries to PerformA
            Marcel tries to PerformB
                Marcel tries to PerformPass
                    Marcel sees if simpleQuestion is equal to True.
    Marcel tries to PerformB
        Marcel tries to PerformPass
            Marcel sees if simpleQuestion is equal to True.
    """
    marcel.will(PerformChatty(PerformA(PerformB(PerformPass()))))
    marcel.will(PerformB(PerformPass()))


def test_passes_with_quietly(marcel: Actor) -> None:
    """
    Generates a quiet log:

    Marcel tries to PerformChatty
    Marcel tries to PerformB
    """
    marcel.will(PerformChatty(Quietly(PerformA(PerformB(PerformPass())))))
    marcel.will(PerformB(Quietly(PerformPass())))


def test_fails_without_quietly(marcel: Actor) -> None:
    """
    Generates a normal log showing failure:

    Marcel tries to PerformChattyFail
        Marcel tries to PerformA
            Marcel tries to PerformB
                Marcel tries to PerformFail
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
    marcel.will(PerformChattyFail(PerformA(PerformB(PerformFail()))))
    marcel.will(PerformB(PerformPass()))


def test_fails_with_quietly(marcel: Actor) -> None:
    """
    Generates a "quiet" log, but demonstrates that in a case of failure the output
    looks identical to a normal log.

    Marcel tries to PerformChattyFail
        Marcel tries to PerformA
            Marcel tries to PerformB
                Marcel tries to PerformFail
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
    marcel.will(PerformChattyFail(Quietly(PerformA(PerformB(PerformFail())))))
    marcel.will(PerformB(Quietly(PerformPass())))


def test_normal_question(marcel: Actor):
    """
    Marcel sees if simpleQuestion is equal to True.
    """
    marcel.will(See(SimpleQuestion(), IsEqual(True)))


def test_fails_question(marcel: Actor):
    """
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
    marcel.will(See(SimpleQuestion(), IsEqual(False)))


def test_exception_in_question(marcel: Actor):
    """
    Marcel sees if simpleQuestionException is equal to False.
        Marcel examines SimpleQuestionException
        ***ERROR***

    Exception: This question raises exception
    """
    marcel.will(See(SimpleQuestionException(), IsEqual(False)))


def test_exception_in_resolution(marcel: Actor):
    """
    Marcel sees if simpleQuestion is equal to True.
        Marcel examines SimpleQuestion
            => True
        ... hoping it's equal to True.
    ***ERROR***

    Exception: This resolution raises exception
    """
    marcel.will(See(SimpleQuestion(), IsEqualButRaisesException(True)))


def test_quiet_see(marcel: Actor):
    """
    * logs absolutely nothing
    """
    marcel.will(Quietly(See(SimpleQuestion(), IsEqual(True))))


def test_fails_quiet_see(marcel: Actor):
    """
    This is a little awkward because of the way it doesn't show ***ERROR***

    Marcel sees if simpleQuestion is equal to False.
        Marcel examines SimpleQuestion
            => True
        ... hoping it's equal to False.
            => <False>
    """
    marcel.will(Quietly(See(SimpleQuestion(), IsEqual(False))))


def test_fails_quiet_question(marcel: Actor):
    """
    This is a little awkward because of the way it doesn't show ***ERROR***

    Marcel sees if simpleQuestion is equal to False.
        ... hoping it's equal to False.
            => <False>
        ***ERROR***

    AssertionError:
    Expected: <False>
         but: was <True>
    """
    marcel.will(See(Quietly(SimpleQuestion()), IsEqual(False)))
