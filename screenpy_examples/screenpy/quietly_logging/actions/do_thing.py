from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy import IsEqual, Performable, beat

from screenpy_examples.screenpy.quietly_logging.actions.see import See
from screenpy_examples.screenpy.quietly_logging.questions import SimpleQuestion

if TYPE_CHECKING:
    from screenpy import Actor


class DoPassAfterAWhile(Performable):
    LIMIT = 5
    COUNTER = 0

    @beat("{} tries to DoPassAfterAWhile")
    def perform_as(self, actor: Actor):
        if DoPassAfterAWhile.COUNTER > DoPassAfterAWhile.LIMIT:
            DoPassAfterAWhile.COUNTER = 0
            return

        DoPassAfterAWhile.COUNTER += 1
        raise AssertionError(f"This is going to Fail {DoPassAfterAWhile.COUNTER}")


class DoFailCounter(Performable):
    COUNTER = 0

    @beat("{} tries to DoFailCounter")
    def perform_as(self, actor: Actor):
        DoFailCounter.COUNTER += 1
        raise AssertionError(f"This is going to Fail {DoFailCounter.COUNTER}")


class DoFail(Performable):
    @beat("{} tries to DoFail")
    def perform_as(self, actor: Actor):
        actor.will(See(SimpleQuestion(), IsEqual(False)))


class PerformPass(Performable):
    @beat("{} tries to PerformPass")
    def perform_as(self, actor: Actor):
        actor.will(See(SimpleQuestion(), IsEqual(True)))


class PerformFirst(Performable):
    @beat("{} tries to PerformFirst")
    def perform_as(self, actor: Actor):
        actor.will(self.action)

    def __init__(self, action: Performable = PerformPass()):
        self.action = action


class PerformSecond(Performable):
    @beat("{} tries to PerformSecond")
    def perform_as(self, actor: Actor):
        actor.will(self.action)

    def __init__(self, action: Performable = PerformPass()):
        self.action = action


class PerformB(Performable):
    @beat("{} tries to PerformB")
    def perform_as(self, actor: Actor):
        actor.will(self.action)

    def __init__(self, action: Performable = PerformPass()):
        self.action = action


class PerformA(Performable):
    @beat("{} tries to PerformA")
    def perform_as(self, actor: Actor):
        actor.will(self.action)

    def __init__(self, action: Performable = PerformB()):
        self.action = action


class PerformChatty(Performable):
    @beat("{} tries to PerformChatty")
    def perform_as(self, actor: Actor):
        actor.will(self.action)

    def __init__(self, action: Performable = PerformA()):
        self.action = action


class PerformChattyFail(Performable):
    @beat("{} tries to PerformChattyFail")
    def perform_as(self, actor: Actor):
        actor.will(self.action)

    def __init__(self, action: Performable = PerformA(PerformB(DoFail()))):
        self.action = action
