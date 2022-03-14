"""
That's a wrap! Stop recording on all cameras.
"""

from screenpy import Actor
from screenpy.pacing import beat

from ..abilities import ControlCameras


class StopRecording:
    """Stops recording on all cameras.

    Examples::

        the_actor.attempts_to(StopRecording())
    """

    @beat("{} stops recording.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to stop recording on all cameras."""
        campy_session = the_actor.ability_to(ControlCameras).campy_session
        for camera in campy_session.cameras:
            camera.thats_a_wrap()
