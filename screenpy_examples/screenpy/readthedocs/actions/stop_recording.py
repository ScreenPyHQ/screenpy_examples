"""
That's a wrap! Stop recording on all cameras.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy.pacing import beat

from screenpy_examples.screenpy.readthedocs.abilities import ControlCameras

if TYPE_CHECKING:
    from screenpy import Actor


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
