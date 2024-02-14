"""
Gather information about the audience's tension.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy_examples.screenpy.readthedocs.abilities import PollTheAudience

if TYPE_CHECKING:
    from screenpy import Actor


class AudienceTension:
    """Ask about the audience's tension levels.

    Examples::

        the_actor.should(See.the(AudienceTension(), IsPalpable())
    """

    def answered_by(self, the_actor: Actor) -> dict:
        """Direct the actor to ask about the audience's tension."""
        pollster = the_actor.ability_to(PollTheAudience).poll_connection
        return pollster.poll_mood()
