"""
Dolly-zoom, that classic tension shot.
https://en.wikipedia.org/wiki/Dolly_zoom
"""

from typing import Optional

from screenpy import Actor, beat

from screenpy_examples.screenpy.readthedocs.abilities import ControlCameras
from screenpy_examples.screenpy.readthedocs.actions import Dolly, Simultaneously, Zoom


class DollyZoom:
    """Perform a dolly zoom (optionally on a character) to enhance drama.

    Examples::

        the_actor.attempts_to(DollyZoom())

        the_actor.attempts_to(DollyZoom.on("Alfred Hitchcock"))
    """

    @staticmethod
    def on(character: str) -> "DollyZoom":
        """Specify the character to put in frame before dolly zooming."""
        return DollyZoom(character)

    @beat("{} executes a thrilling dolly zoom{detail}!")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to dolly zoom on their camera."""
        if self.character:
            campy_session = the_actor.ability_to(ControlCameras).campy_session
            camera = campy_session.get_camera_on_character(self.character)
            zoom = Zoom.in_().on_camera(camera)
        else:
            zoom = Zoom.in_()

        the_actor.attempts_to(
            Simultaneously(
                Dolly().backward(),
                zoom,
            ),
        )

    def __init__(self, character: Optional[str] = None) -> None:
        self.character = character
        self.detail = f" on {character}" if character else ""
