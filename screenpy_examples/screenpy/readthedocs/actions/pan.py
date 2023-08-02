"""
Pan using the active camera.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy.pacing import beat

from screenpy_examples.screenpy.readthedocs.abilities import ControlCameras

if TYPE_CHECKING:
    from screenpy import Actor


class Pan:
    """Pan on the active camera.

    Examples::

        the_actor.attempts_to(Pan.left())

        the_actor.attempts_to(Pan.right())
    """

    @staticmethod
    def left() -> "Pan":
        """Pan left!."""
        return Pan(-1, "left")

    @staticmethod
    def right() -> "Pan":
        """Pan right!"""
        return Pan(1, "right")

    @beat("{} pans {description}.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to pan the active camera."""
        campy_session = the_actor.ability_to(ControlCameras).campy_session
        camera = campy_session.get_active_camera()

        camera.pan(self.direction)

    def __init__(self, direction: int, description: str) -> None:
        self.direction = direction
        self.description = description
