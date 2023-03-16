from __future__ import annotations
from screenpy import Actor
from screenpy.protocols import Answerable


class SimpleQuestion(Answerable):
    def answered_by(self, actor: Actor):
        return True
