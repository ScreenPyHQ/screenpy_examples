import contextlib
import io
import logging
import os
import sys
import traceback
from typing import Type

import hamcrest
import hamcrest.core.base_matcher

import screenpy.actions
import screenpy.actor
import screenpy.narration.adapters
import screenpy.narration.narrator
import screenpy.resolutions

__logger: Type[logging.Logger] = logging.getLoggerClass()


CRITICAL = logging.CRITICAL  # 50
FATAL = logging.FATAL  # 50
ERROR = logging.ERROR  # 40
WARNING = logging.WARNING  # 30
WARN = logging.WARNING  # 30
INFO = logging.INFO  # 20
DEBUG = logging.DEBUG  # 10
TRACE = DEBUG - 5  # 5


if hasattr(sys, '_getframe'):
    currentframe = lambda: sys._getframe(3)
else:  #pragma: no cover
    def currentframe():
        """Return the frame object for the caller's stack frame."""
        try:
            raise Exception
        except Exception:
            return sys.exc_info()[2].tb_frame.f_back


def mod_path(function):
    return os.path.normcase(function.__code__.co_filename)


# ignored_modules = [
#     "contextlib.py",
#     "nxt_logger.py",
#     # screenpy
#     "stdout_adapter.py",
#     "pacing.py",
#     "narrator.py",
#     "actor.py",
#     "eventually.py",
#     "see.py",
#     # hamcrest
#     "base_matcher.py",
#     "assert_that.py",
# ]

# ignore_srcfiles is used when walking the stack to check when we've got the first
# caller stack frame, by skipping frames whose filename is listed.

# Ordinarily we would use __file__ for this, but frozen modules don't always
# have __file__ set, for some reason (see Issue #21736). Thus, we get the
# filename from a handy code object from a function defined each module.

# when adding functions to this list, you must avoid those which have decorators.
ignore_srcfiles = [
    mod_path(mod_path),
    mod_path(contextlib.contextmanager),
    mod_path(screenpy.narration.adapters.stdout_adapter.StdOutAdapter.aside),
    mod_path(screenpy.pacing.act),
    mod_path(screenpy.narration.narrator._chainify),
    mod_path(screenpy.actor.Actor.who_can),
    mod_path(screenpy.actions.eventually.Eventually.describe),
    mod_path(screenpy.actions.see.See.describe),
    mod_path(screenpy.resolutions.base_resolution.BaseResolution.get_line),
    mod_path(hamcrest.core.base_matcher.BaseMatcher.matches),
    mod_path(hamcrest.assert_that),
    mod_path(hamcrest.core.core.isnot.is_not),
]


class ScreenpyLogger(__logger):  # type: ignore
    TRACE = TRACE
    CRITICAL = CRITICAL
    FATAL = FATAL
    ERROR = ERROR
    WARNING = WARNING
    WARN = WARN
    INFO = INFO
    DEBUG = DEBUG
    TRACE = TRACE

    def __init__(self, name, level=DEBUG):
        super().__init__(name, level)
        self.__add_level_name("TRACE", TRACE)

    @staticmethod
    def __add_level_name(name: str, level: int):
        logging.addLevelName(level, name)
        setattr(logging, name, level)

    def __log(self, level: int, msg: str, *args, **kwargs):
        if self.isEnabledFor(level):
            if ignore_srcfiles:
                fn, lno, func, sinfo = self.findCaller()
                file_line = f"{os.path.basename(fn)}:{lno}"
            else:
                file_line = "(unknown file):0"
            extra = {"fileline": file_line}
            self._log(level, msg, args, **kwargs, extra=extra)

    def log(self, level: int, msg: str, *args, **kwargs) -> None:
        self.__log(level, msg, *args, **kwargs)

    def trace(self, msg: str, *args, **kwargs):
        self.__log(TRACE, msg, *args, **kwargs)

    def debug(self, msg: str, *args, **kwargs):
        self.__log(DEBUG, msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs):
        self.__log(INFO, msg, *args, **kwargs)

    def findCaller(self, stack_info=False, stacklevel=1):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = currentframe()
        #On some versions of IronPython, currentframe() returns None if
        #IronPython isn't run with -X:Frames.
        if f is not None:
            f = f.f_back
        orig_f = f
        while f and stacklevel > 1:
            f = f.f_back
            stacklevel -= 1
        if not f:
            f = orig_f
        rv = "(unknown file)", 0, "(unknown function)", None
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename in ignore_srcfiles:
                f = f.f_back
                continue
            sinfo = None
            if stack_info:
                sio = io.StringIO()
                sio.write('Stack (most recent call last):\n')
                traceback.print_stack(f, file=sio)
                sinfo = sio.getvalue()
                if sinfo[-1] == '\n':
                    sinfo = sinfo[:-1]
                sio.close()
            rv = (co.co_filename, f.f_lineno, co.co_name, sinfo)
            break
        return rv


def create_logger(name: str) -> ScreenpyLogger:
    logging.setLoggerClass(ScreenpyLogger)
    # pycharm gets confused about getLogger returning ScreenpyLogger.
    # mypy also doesn't understand this since it is a dynamic call.
    logger: ScreenpyLogger = logging.getLogger(name)  # type: ignore
    # logging.setLoggerClass(ScreenpyLogger)
    logging.setLoggerClass(__logger)
    logger.setLevel(DEBUG)
    logger.propagate = True
    return logger
