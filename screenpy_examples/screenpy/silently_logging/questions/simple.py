from __future__ import annotations

from typing import NoReturn

from screenpy import Actor, Answerable, beat


class SimpleQuestion(Answerable):
    @beat("{} examines SimpleQuestion")
    def answered_by(self, _: Actor) -> bool:
        return True

    def describe(self) -> str:
        return "SimpleQuestion"


class SimpleQuestionException(Answerable):
    @beat("{} examines SimpleQuestionException")
    def answered_by(self, _: Actor) -> NoReturn:
        raise Exception("This question raises exception")

    def describe(self) -> str:
        return "SimpleQuestionException"
