from __future__ import annotations

from screenpy import Actor, Answerable, beat


class SimpleQuestion(Answerable):
    @beat("{} examines SimpleQuestion")
    def answered_by(self, actor: Actor) -> bool:
        return True

    def describe(self) -> str:
        return "SimpleQuestion"


class SimpleQuestionException(Answerable):
    @beat("{} examines SimpleQuestionException")
    def answered_by(self, actor: Actor):
        raise Exception("This question raises exception")

    def describe(self):
        return "SimpleQuestionException"
