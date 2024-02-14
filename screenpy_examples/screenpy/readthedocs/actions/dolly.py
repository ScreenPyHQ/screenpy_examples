"""
Dolly a camera in a direction.
"""

from __future__ import annotations

from screenpy import Actor, UnableToAct, beat

from screenpy_examples.screenpy.readthedocs.abilities import ControlCameras


class Dolly:
    """Dolly a camera in a direction.

    Examples::

        the_actor.attempts_to(Dolly().left())

        the_actor.attempts_to(Dolly().backwards())

        the_actor.attempts_to(Dolly().forward().right())
    """

    def __init__(self) -> None:
        self.vector: tuple[int, int] = (0, 0)

    def forward(self) -> Dolly:
        """Dolly forward!"""
        self.vector = (self.vector[0], self.vector[1] + 1)
        return self

    def backward(self) -> Dolly:
        """Dolly backward!"""
        self.vector = (self.vector[0], self.vector[1] - 1)
        return self

    def left(self) -> Dolly:
        """Dolly left!"""
        self.vector = (self.vector[0] - 1, self.vector[1])
        return self

    def right(self) -> Dolly:
        """Dolly right!"""
        self.vector = (self.vector[0] + 1, self.vector[1])
        return self

    @property
    def description(self) -> str:
        direction = ""
        if self.vector[1] >= 1:
            direction = "forward"
        elif self.vector[1] <= -1:
            direction = "backward"

        if direction and self.vector[0] != 0:
            direction += "-"

        if self.vector[0] >= 1:
            direction += "right"
        elif self.vector[0] <= -1:
            direction += "left"

        return direction

    @beat("{} dollies the active camera {description}.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to dolly their active camera."""
        if self.vector == (0, 0):
            msg = "No direction was given to Dolly!"
            raise UnableToAct(msg)

        campy_session = the_actor.ability_to(ControlCameras).campy_session
        camera = campy_session.get_active_camera()

        camera.dolly(*self.vector)
