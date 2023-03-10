from screenpy_examples.screenpy.readthedocs import cam_py


class ControlCameras:
    """Enable an Actor to control cameras through cam_py.

    Examples::

        the_actor.can(ControlCameras())
    """

    def __init__(self) -> None:
        self.campy_session = cam_py.RecordingSession()
        self.cameras = []

    def forget(self) -> None:
        for camera in self.cameras:
            camera.stop()
        self.campy_session.wrap()
