from __future__ import annotations

from screenpy import BaseResolution

from .matchers.has_saturation_greater_than import is_palpable


class IsPalpable(BaseResolution):
    """Match a tension level that is very, very high!!!

    Examples::

        the_actor.should(See.the(AudienceTension(), IsPalpable()))
    """

    line = "a palpable tension!"
    matcher_function = is_palpable
