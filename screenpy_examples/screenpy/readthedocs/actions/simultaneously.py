"""
Perform one or more camera actions simultaneously.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy import beat

from screenpy_examples.screenpy.readthedocs.abilities import ControlCameras

if TYPE_CHECKING:
    from screenpy import Actor, Performable


class Simultaneously:
    """Simultaneously perform many camera actions.

    Examples::

        the_actor.attempts_to(
            Simultaneously(
                Dolly().forward(),
                Pan.left(),
                Zoom.out(),
            )
        )
    """

    @beat("{} performs some thrilling camerawork simultaneously!")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to perform several actions at once."""
        campy_session = the_actor.ability_to(ControlCameras).campy_session

        with campy_session.simultaneous_movement:
            the_actor.attempts_to(*self.actions)

    def __init__(self, *actions: Performable) -> None:
        self.actions = actions
