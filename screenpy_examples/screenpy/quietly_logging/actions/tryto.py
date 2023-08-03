from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

from screenpy import Performable, the_narrator

if TYPE_CHECKING:
    from screenpy import Actor


class TryTo(Performable):
    Second: Tuple[Performable, ...]

    def perform_as(self, actor: Actor):
        # Since we are fully expecting assertion error to be raised we kink the
        # cable to avoid the explanation; which only happens when the cable is not
        # kinked

        # logs the first attempt only if it succeeds.
        with the_narrator.mic_cable_kinked():
            try:
                actor.will(*self.First)
                return
            except AssertionError:
                the_narrator.clear_backup()

        actor.will(*self.Second)
        return

    def or_(self, *second: Performable):
        self.Second = second
        return self

    else_ = otherwise = alternatively = failing_that = or_

    def __init__(self, *first: Performable):
        self.First: Tuple[Performable, ...] = first


Either = SeeIfTheyCan = Attempt = AttemptTo = GoFor = Try = TryTo
