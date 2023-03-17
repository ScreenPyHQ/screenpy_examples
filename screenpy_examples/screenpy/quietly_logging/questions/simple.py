from __future__ import annotations
from screenpy import Actor, beat
from screenpy.protocols import Answerable


class SimpleQuestion(Answerable):
    @beat("{} examines SimpleQuestion")
    def answered_by(self, actor: Actor):
        return True
