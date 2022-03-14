import pollster


class PollTheAudience:
    """Enable Actors to poll the audience.

    Examples::

        the_actor.can(PollTheAudience())
    """

    def __init__(self):
        self.poll_connection = pollster.connect_to_audience()

    def forget(self):
        self.poll_connection.close()
