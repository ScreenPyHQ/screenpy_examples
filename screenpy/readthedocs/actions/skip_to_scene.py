"""
Skip to a specific scene while recording.
"""

from screenpy import Actor
from screenpy.pacing import beat

from ..abilities import ControlCameras


class SkipToScene:
    """Skips to a numbered scene in a screenplay.

    Examples::

        the_actor.attempts_to(SkipToScene(2))
    """

    @beat("{} skips to scene #{scene_num}.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to skip to a specific scene."""
        cameras = the_actor.ability_to(ControlCameras).cameras

        for camera in cameras:
            camera.set_the_scene(self.scene_num)

    def __init__(self, scene_num: int) -> None:
        self.scene_num = scene_num
