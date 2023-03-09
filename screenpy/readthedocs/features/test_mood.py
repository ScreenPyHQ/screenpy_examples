"""
Test our ability to influence the audience's mood with skillful camerawork.
"""

from ..cam_py import Camera
from screenpy import AnActor, given, then, when
from screenpy.actions import See
from screenpy.resolutions import Equals

from ..actions import (
    JumpToCamera,
    Dolly,
    Pan,
    SkipToScene,
    StartRecording,
    StopRecording,
    Zoom,
)
from ..constants import LAUGHING
from ..tasks import CutToCloseup, DollyZoom
from ..questions import AudienceTension, TopAudienceReaction
from ..resolutions import IsPalpable
from ..scripts import GOOD_WILL_HUNTING, SHAUN_OF_THE_DEAD


def test_dramatic_moment(Cameron: AnActor, Polly: AnActor) -> None:
    """We can use the camera to create dramatic tension."""
    Cameron.has_cleanup_tasks(StopRecording())

    given(Cameron).was_able_to(
        StartRecording(GOOD_WILL_HUNTING).on(Camera("Will")),
        SkipToScene(35),
    )

    when(Cameron).attempts_to(
        Dolly().left(),
        CutToCloseup.on("Will"),
        DollyZoom(),
    )

    then(Polly).should(See.the(AudienceTension(), IsPalpable()))


def test_comedic_timing(Cameron: AnActor, Polly: AnActor) -> None:
    """We can use the camera to make funny moments."""
    Cameron.has_cleanup_tasks(StopRecording())
    one = Camera("Shaun")
    two = Camera("Ed")

    given(Cameron).was_able_to(
        StartRecording(SHAUN_OF_THE_DEAD).on(one).and_(two),
        SkipToScene(20),
    )

    when(Cameron).attempts_to(
        Zoom.in_().on_camera(one),
        JumpToCamera(two),
        Zoom.out().on_camera(two),
        JumpToCamera(one),
        Pan.left(),
        JumpToCamera(two),
        JumpToCamera(one),
    )

    then(Polly).should(See.the(TopAudienceReaction(), Equals(LAUGHING)))
