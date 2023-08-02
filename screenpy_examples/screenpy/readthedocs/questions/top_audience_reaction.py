"""
Gather information about the audience's tension.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy_examples.screenpy.readthedocs.abilities import PollTheAudience

if TYPE_CHECKING:
    from screenpy import Actor


class TopAudienceReaction:
    """Ask about the audience's most popular reaction.

    Examples::

        the_actor.should(See.the(TopAudienceReaction(), Equals(LAUGHING))
    """

    def answered_by(self, the_actor: Actor) -> str:
        """Direct the actor to ask about the audience's top mood."""
        pollster = the_actor.ability_to(PollTheAudience).poll_connection
        return pollster.poll_mood().top_mood
