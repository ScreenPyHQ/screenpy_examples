from __future__ import annotations

from typing import Any, Optional, Tuple, TypeVar

from hamcrest.core.base_matcher import BaseMatcher, Matcher

from screenpy import Actor
from screenpy.pacing import the_narrator
from screenpy.protocols import Answerable, Performable  , Resolvable


T = TypeVar("T")
DEBUG_MODE = False


class QuietlyMixin:
    def __getattr__(self, key):
        try:
            return super().__get_attribute__(key)
        except AttributeError:
            return getattr(self.duck, key)


class QuietlyPerformable(Performable, QuietlyMixin):
    def perform_as(self, actor: Actor) -> None:
        with the_narrator.mic_cable_kinked():
            self.duck.perform_as(actor)
            the_narrator.clear_backup()
            return

    def __init__(self, duck: Performable):
        self.duck = duck


class QuietlyAnswerable(Answerable, QuietlyMixin):
    def answered_by(self, actor: Actor) -> Any:
        with the_narrator.mic_cable_kinked():
            thing = self.duck.answered_by(actor)
            the_narrator.clear_backup()
            return thing

    def __init__(self, duck: Answerable):
        self.duck = duck


class QuietlyResolvable(Resolvable, QuietlyMixin):
    def resolve(self) -> Matcher:
        with the_narrator.mic_cable_kinked():
            res = self.duck.resolve()
            the_narrator.clear_backup()
            return res

    def __init__(self, duck: Resolvable):
        self.duck = duck


T_duck = Performable | Answerable | Resolvable
T_Q = QuietlyAnswerable | QuietlyPerformable | QuietlyResolvable


def __Quietly(duck: T_duck) -> T_duck | T_Q:
    if isinstance(duck, Performable):
        return QuietlyPerformable(duck)
    elif isinstance(duck, Answerable):
        return QuietlyAnswerable(duck)
    elif isinstance(duck, Resolvable):
        return QuietlyResolvable(duck)
    else:
        return duck


def Quietly(
    duck: T_duck | Tuple[T_duck, ...]
) -> T_duck | Tuple[T_duck, ...] | T_Q | Tuple[T_Q, ...]:
    if DEBUG_MODE:
        return duck
    if isinstance(duck, tuple):
        l = []
        for d in duck:
            l.append(__Quietly(d))
        return tuple(l)
    else:
        return __Quietly(duck)
