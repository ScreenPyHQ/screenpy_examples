"""
Warning about using filename and lineno in logging in virtual environments.
Python pycache stores the path information of modules based upon how python was called.
If python was called using it's symlink, pycache will store the symlink paths.
If python was called using it's real path, pycache will store the real paths.

Running python one way then the other (symlink then real or real then symlink) can lead
to the logged filename and line numbers to be incorrect. When this occurs, clean out the
pycache.  Or just run without caching enabled. PYTHONDONTWRITEBYTECODE=1

"""

from __future__ import annotations

import contextlib
import io
import logging
import os
import sys
import traceback
from types import FrameType, FunctionType, TracebackType
from typing import Callable, Type, cast, TYPE_CHECKING, TypeAlias, Mapping, Any

import hamcrest
import hamcrest.core.base_matcher
import screenpy.actions
import screenpy.actor
import screenpy.narration.narrator
import screenpy.narration.stdout_adapter
import screenpy.resolutions

import screenpy_examples.screenpy.silently_logging.actions.see


if TYPE_CHECKING:
    T_exc: TypeAlias = (
        tuple[type[BaseException], BaseException, TracebackType | None]
        | tuple[None, None, None]
        | None
    )

__logger: Type[logging.Logger] = logging.getLoggerClass()
_logRecordFactory = logging.getLogRecordFactory()


ALL = logging.CRITICAL * 10  # 500 #IO  # Trace.always
STDERR = logging.CRITICAL * 2  # 100
STDOUT = STDERR - 10  # 90
CRITICAL = logging.CRITICAL  # 50
FATAL = logging.FATAL  # 50
ERROR = logging.ERROR  # 40
WARNING = logging.WARNING  # 30
WARN = logging.WARNING  # 30
INFO = logging.INFO  # 20
DEBUG = logging.DEBUG  # 10
TRACE = DEBUG - 5  # 5
NOTSET = logging.NOTSET  # 0


if hasattr(sys, "_getframe"):

    def currentframe() -> FrameType:
        return sys._getframe(3)

else:  # pragma: no cover

    def currentframe() -> FrameType:
        """Return the frame object for the caller's stack frame."""
        try:
            raise Exception
        except Exception:
            rt = sys.exc_info()
            return rt[2].tb_frame.f_back  # type: ignore


def mod_path(function: FunctionType | Callable) -> str:
    return os.path.normcase(function.__code__.co_filename)


ignore_srcfiles = [
    mod_path(mod_path),
    mod_path(contextlib.contextmanager),
    mod_path(screenpy.narration.stdout_adapter.StdOutAdapter.aside),
    mod_path(screenpy.pacing.act),
    mod_path(screenpy.narration.narrator._chainify),
    mod_path(screenpy.actor.Actor.named),
    mod_path(screenpy.actions.eventually.Eventually.describe),
    mod_path(screenpy.actions.either.Either.or_),
    mod_path(screenpy.actions.see.See.describe),
    mod_path(screenpy_examples.screenpy.silently_logging.actions.see.See.describe),
    mod_path(hamcrest.core.base_matcher.BaseMatcher.matches),
    mod_path(hamcrest.assert_that),
    mod_path(hamcrest.core.core.isnot.is_not),
]


class ScreenpyLogger(__logger):  # type: ignore
    TRACE = TRACE
    ALL = ALL
    STDERR = STDERR
    STDOUT = STDOUT
    CRITICAL = CRITICAL
    FATAL = FATAL
    ERROR = ERROR
    WARNING = WARNING
    WARN = WARN
    INFO = INFO
    DEBUG = DEBUG
    NOTSET = NOTSET
    timestamp_format = "%Y-%m-%dT%H-%M-%S"

    def __init__(self, name: str, level: int = NOTSET) -> None:
        super().__init__(name, level)
        self.__add_level_name("TRACE", TRACE)

    @staticmethod
    def __add_level_name(name: str, level: int) -> None:
        logging.addLevelName(level, name)
        setattr(logging, name, level)

    def __log(self, level: int, msg: object, *args: Any, **kwargs: Any) -> None:
        if self.isEnabledFor(level):
            if ignore_srcfiles:
                fn, lno, func, sinfo = self.findCaller()
                file_line = f"{os.path.basename(fn)}:{lno}"
            else:
                file_line = "(unknown file):0"

            extra = {"fileline": file_line} | kwargs.pop("extra", {})
            self._log(level, msg, args, **kwargs, extra=extra)

    def makeRecord(
        self,
        name: str,
        level: int,
        fn: str,
        lno: int,
        msg: object,
        args: tuple[object, ...] | Mapping[str, object] | None,
        exc_info: T_exc,
        func: str | None = None,
        extra: dict | None = None,
        sinfo: str | None = None,
    ) -> logging.LogRecord:
        """
        bypassing restrictions to override created timestamp
        """
        rv = _logRecordFactory(name, level, fn, lno, msg, args, exc_info, func, sinfo)
        if extra is not None:
            for key in extra:
                rv.__dict__[key] = extra[key]
        return rv

    def log(self, level: int, msg: object, *args: Any, **kwargs: Any) -> None:
        self.__log(level, msg, *args, **kwargs)

    def trace(self, msg: object, *args: Any, **kwargs: Any) -> None:
        self.__log(TRACE, msg, *args, **kwargs)

    def debug(self, msg: object, *args: Any, **kwargs: Any) -> None:
        self.__log(DEBUG, msg, *args, **kwargs)

    def info(self, msg: object, *args: Any, **kwargs: Any) -> None:
        self.__log(INFO, msg, *args, **kwargs)

    def print_stack_trace(self) -> None:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        str_list = traceback.format_exception(exc_type, exc_value, exc_traceback)
        self.critical("".join(str_list))

    def findCaller(
        self, stack_info: bool = False, stacklevel: int = 1
    ) -> tuple[str, int, str, str | None]:
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = currentframe()
        # On some versions of IronPython, currentframe() returns None if
        # IronPython isn't run with -X:Frames.
        if f is not None:
            f = cast(FrameType, f.f_back)

        orig_f: FrameType = f
        while f and stacklevel > 1:
            f = f.f_back  # type: ignore
            stacklevel -= 1
        if not f:
            f = orig_f
        rv: tuple[str, int, str, str | None]
        rv = "(unknown file)", 0, "(unknown function)", None
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename in ignore_srcfiles:
                f = cast(FrameType, f.f_back)
                continue
            sinfo = None
            if stack_info:
                sio = io.StringIO()
                sio.write("Stack (most recent call last):\n")
                traceback.print_stack(f, file=sio)
                sinfo = sio.getvalue()
                if sinfo[-1] == "\n":
                    sinfo = sinfo[:-1]
                sio.close()
            rv = (co.co_filename, f.f_lineno, co.co_name, sinfo)
            break
        return rv


def create_logger(name: str = "scrnpy") -> ScreenpyLogger:
    # NOTE: do not use "screenpy" for logger name. It already exists.
    logging.setLoggerClass(ScreenpyLogger)
    # pycharm gets confused about getLogger returning ScreenpyLogger.
    # mypy also doesn't understand this since it is a dynamic call.
    logger: ScreenpyLogger = logging.getLogger(name)  # type: ignore
    logger.setLevel(DEBUG)
    logger.propagate = True
    return logger
