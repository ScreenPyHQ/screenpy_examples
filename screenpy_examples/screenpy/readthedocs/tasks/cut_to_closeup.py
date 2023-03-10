"""
Cut to a closeup for some personal reactions.
"""

from screenpy import Actor
from screenpy.pacing import beat

from screenpy_examples.screenpy.readthedocs.abilities import ControlCameras
from screenpy_examples.screenpy.readthedocs.actions import JumpToCamera, Zoom


class CutToCloseup:
    """Cut to a closeup on a character.

    Examples::

        the_actor.attempts_to(CutToCloseup.on("Rizzo"))
    """

    @staticmethod
    def on(character: str) -> "CutToCloseup":
        """Specify the character to cut to."""
        return CutToCloseup(character)

    @beat("{} cuts to a closeup on {character}!")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to cut to a closeup on a character."""
        campy_session = the_actor.ability_to(ControlCameras).campy_session
        camera = campy_session.get_camera_on_character(self.character)
        camera.character = self.character  # ignore this line, it makes the logs nice

        the_actor.attempts_to(
            Zoom.in_().on_camera(camera),  # note this camera may not be active
            JumpToCamera(camera),
        )

    def __init__(self, character: str) -> None:
        self.character = character
