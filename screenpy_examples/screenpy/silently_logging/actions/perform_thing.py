from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy import IsEqual, Performable, beat

from screenpy_examples.screenpy.silently_logging.actions.see import See
from screenpy_examples.screenpy.silently_logging.questions import SimpleQuestion

if TYPE_CHECKING:
    from screenpy import Actor


class PerformPassAfterAWhile(Performable):
    LIMIT = 5
    COUNTER = 0

    @beat("{} tries to PerformPassAfterAWhile")
    def perform_as(self, actor: Actor):
        if PerformPassAfterAWhile.COUNTER > PerformPassAfterAWhile.LIMIT:
            PerformPassAfterAWhile.COUNTER = 0
            return

        PerformPassAfterAWhile.COUNTER += 1
        raise AssertionError(f"This is going to Fail {PerformPassAfterAWhile.COUNTER}")


class PerformFailCounter(Performable):
    COUNTER = 0

    @beat("{} tries to PerformFailCounter")
    def perform_as(self, actor: Actor):
        PerformFailCounter.COUNTER += 1
        raise AssertionError(f"This is going to Fail {PerformFailCounter.COUNTER}")


class PerformFail(Performable):
    @beat("{} tries to PerformFail")
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

    def __init__(self, action: Performable = PerformA(PerformB(PerformFail()))):
        self.action = action
