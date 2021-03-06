"""
Zoom in/out on the active camera.
"""

import cam_py
from screenpy import Actor
from screenpy.pacing import beat

from ..abilities import ControlCameras


class Zoom:
    """Zoom in or out on the active camera.

    Examples::

        the_actor.attempts_to(Zoom.out())

        the_actor.attempts_to(Zoom.in_())

        the_actor.attempts_to(Zoom.in_().on("Norman Bates"))
    """

    @staticmethod
    def out() -> "Zoom":
        """Zoom out!"""
        return Zoom(-1, "out")

    @staticmethod
    def in_() -> "Zoom":
        """Zoom in!"""
        return Zoom(1, "in")

    def on_camera(self, camera: cam_py.Camera) -> "Zoom":
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
