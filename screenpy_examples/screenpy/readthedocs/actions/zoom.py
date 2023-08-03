"""
Zoom in/out on the active camera.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy.pacing import beat

from screenpy_examples.screenpy.readthedocs.abilities import ControlCameras

if TYPE_CHECKING:
    from unittest import mock

    from screenpy import Actor


class Zoom:
    """Zoom in or out on the active camera.

    Examples::

        the_actor.attempts_to(Zoom.out())

        the_actor.attempts_to(Zoom.in_())

        the_actor.attempts_to(Zoom.in_().on("Norman Bates"))
    """
    camera: mock.MagicMock | None

    @staticmethod
    def out() -> "Zoom":
        """Zoom out!"""
        return Zoom(-1, "out")

    @staticmethod
    def in_() -> "Zoom":
        """Zoom in!"""
        return Zoom(1, "in")

    def on_camera(self, camera: mock.MagicMock) -> "Zoom":
        """Zoom in on a specific camera (camera)."""
        self.camera = camera
        return self

    @beat("{} zooms {description}.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to pan the active camera."""
        campy_session = the_actor.ability_to(ControlCameras).campy_session
        if self.camera is None:
            self.camera = campy_session.get_active_camera()

        self.camera.zoom(self.direction)

    def __init__(self, direction: int, description: str) -> None:
        self.direction = direction
        self.description = description
        self.camera = None
