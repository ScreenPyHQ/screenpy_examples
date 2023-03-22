import pytest

from screenpy import Actor
from screenpy.actions import Eventually
from screenpy.resolutions import IsEqual

from screenpy_examples.screenpy.quietly_logging.actions import (
    DoA,
    DoB,
    DoChatty,
    DoChattyFail,
    DoFail,
    DoFailCounter,
    DoPass,
    DoPassAfterAWhile,
    Quietly,
    See,
)
from screenpy_examples.screenpy.quietly_logging.questions import (
    SimpleQuestion,
    SimpleQuestionException,
)
from screenpy_examples.screenpy.quietly_logging.resolutions import IsEqualButRaisesException


def test_eventually_succeeds(marcel: Actor) -> None:
    marcel.will(Eventually(DoPassAfterAWhile()).for_(1).seconds())


def test_eventually_fails(marcel: Actor) -> None:
    marcel.will(Eventually(DoFailCounter()).for_(1).seconds())


## TODO: remove this comment after pr is merged
## all of the exmaples below are using the refactor-resolutions branch
## https://github.com/ScreenPyHQ/screenpy/pull/57

def test_passes_without_quietly(marcel: Actor) -> None:
    """
    Generates a normal log:

    Marcel tries to DoChatty
        Marcel tries to DoA
            Marcel tries to DoB
                Marcel tries to DoPass
                    Marcel sees if simpleQuestion is equal to True.
    Marcel tries to DoB
        Marcel tries to DoPass
            Marcel sees if simpleQuestion is equal to True.
    """
    marcel.will(DoChatty(DoA(DoB(DoPass()))))
    marcel.will(DoB(DoPass()))


def test_passes_with_quietly(marcel: Actor) -> None:
    """
    Generates a quiet log:

    Marcel tries to DoChatty
    Marcel tries to DoB
    """
    marcel.will(DoChatty(Quietly(DoA(DoB(DoPass())))))
    marcel.will(DoB(Quietly(DoPass())))


def test_fails_without_quietly(marcel) -> None:
    """
    Generates a normal log showing failure:

    Marcel tries to DoChattyFail
        Marcel tries to DoA
            Marcel tries to DoB
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
    marcel.will(DoChattyFail(DoA(DoB(DoFail()))))
    marcel.will(DoB(DoPass()))


def test_fails_with_quietly(marcel) -> None:
    """
    Generates a "quiet" log, but demonstrates that in a case of failure the output
    looks identical to a normal log.

    Marcel tries to DoChattyFail
        Marcel tries to DoA
            Marcel tries to DoB
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
    marcel.will(DoChattyFail(Quietly(DoA(DoB(DoFail())))))
    marcel.will(DoB(Quietly(DoPass())))


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
