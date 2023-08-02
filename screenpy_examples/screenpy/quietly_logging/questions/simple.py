from __future__ import annotations

from screenpy import Actor, beat
from screenpy.protocols import Answerable


class SimpleQuestion(Answerable):
    @beat("{} examines SimpleQuestion")
    def answered_by(self, actor: Actor):
        return True

    def describe(self):
        return "SimpleQuestion"


class SimpleQuestionException(Answerable):
    @beat("{} examines SimpleQuestionException")
    def answered_by(self, actor: Actor):
        raise Exception("This question raises exception")

    def describe(self):
        return "SimpleQuestionException"
