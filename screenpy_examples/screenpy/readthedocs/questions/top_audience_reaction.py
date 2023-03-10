"""
Gather information about the audience's tension.
"""

from screenpy import Actor

from ..abilities import PollTheAudience


class TopAudienceReaction:
    """Ask about the audience's most popular reaction.

    Examples::

        the_actor.should(See.the(TopAudienceReaction(), Equals(LAUGHING))
    """

    def answered_by(self, the_actor: Actor) -> str:
        """Direct the actor to ask about the audience's top mood."""
        pollster = the_actor.ability_to(PollTheAudience).poll_connection
        return pollster.poll_mood().top_mood
