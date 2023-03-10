"""
Start recording a screenplay on one or more cameras!
"""

from .. import cam_py
from screenpy import Actor
from screenpy.pacing import beat

from ..abilities import ControlCameras


class StartRecording:
    """Starts recording on one or more cameras.

    Examples::

        the_actor.attempts_to(StartRecording())

        camera = Camera("Character")
        the_actor.attempts_to(StartRecording.on(camera))

        camera1 = Camera("Character1")
        camera2 = Camera("Character2")
        the_actor.attempts_to(StartRecording.on(camera1).and_(camera2))
    """

    def on(self, camera: cam_py.Camera) -> "StartRecording":
        """Record on an already-created camera."""
        self.cameras.append(camera)
        return self

    and_ = on

    @beat("{} starts recording on {cameras_to_log}.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to start recording on their cameras."""
        if not self.cameras:
            self.cameras = [cam_py.Camera("Main")]

        campy_session = the_actor.ability_to(ControlCameras).campy_session
        for camera in self.cameras:
            camera.record(self.script)
            campy_session.add_camera(camera)

    @property
    def cameras_to_log(self) -> str:
        """Get a nice list of all the cameras for the logged beat."""
        return ", ".join(camera.character for camera in self.cameras)

    def __init__(self, script: str) -> None:
        self.script = script
        self.cameras = []
