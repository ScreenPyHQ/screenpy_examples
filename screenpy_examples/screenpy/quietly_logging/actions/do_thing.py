from __future__ import annotations

from screenpy import Actor
from screenpy.pacing import beat
from screenpy.protocols import Performable
from screenpy.resolutions import IsEqual

from screenpy_examples.screenpy.quietly_logging.actions.see import See
from screenpy_examples.screenpy.quietly_logging.questions import SimpleQuestion


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


class DoPass(Performable):
    @beat("{} tries to DoPass")
    def perform_as(self, actor: Actor):
        actor.will(See(SimpleQuestion(), IsEqual(True)))


class DoFirst(Performable):
    @beat("{} tries to DoFirst")
    def perform_as(self, actor: Actor):
        actor.will(self.action)

    def __init__(self, action: Performable = DoPass()):
        self.action = action


class DoSecond(Performable):
    @beat("{} tries to DoSecond")
    def perform_as(self, actor: Actor):
        actor.will(self.action)

    def __init__(self, action: Performable = DoPass()):
        self.action = action


class DoB(Performable):
    @beat("{} tries to DoB")
    def perform_as(self, actor: Actor):
        actor.will(self.action)

    def __init__(self, action: Performable = DoPass()):
        self.action = action


class DoA(Performable):
    @beat("{} tries to DoA")
    def perform_as(self, actor: Actor):
        actor.will(self.action)

    def __init__(self, action: Performable = DoB()):
        self.action = action


class DoChatty(Performable):
    @beat("{} tries to DoChatty")
    def perform_as(self, actor: Actor):
        actor.will(self.action)

    def __init__(self, action: Performable = DoA()):
        self.action = action


class DoChattyFail(Performable):
    @beat("{} tries to DoChattyFail")
    def perform_as(self, actor: Actor):
        actor.will(self.action)

    def __init__(self, action: Performable = DoA(DoB(DoFail()))):
        self.action = action
