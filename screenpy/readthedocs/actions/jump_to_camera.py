"""
Set the active camera.
"""

import cam_py
from screenpy import Actor
from screenpy.pacing import beat

from ..abilities import ControlCameras


class JumpToCamera:
    """Jump to a different camera (set the active camera).

    Examples::

        the_actor.attempts_to(JumpToCamera(two))
    """

    @beat("{} jumps to the camera on {character}!")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to jump to another camera."""
        campy_session = the_actor.ability_to(ControlCameras).campy_session
        campy_session.set_active_camera(self.camera)

    def __init__(self, camera: cam_py.Camera) -> None:
        self.camera = camera
        self.character = camera.character
