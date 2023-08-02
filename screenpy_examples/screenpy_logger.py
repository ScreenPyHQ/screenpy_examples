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
import inspect
import io
import logging
import os
import sys
import traceback
from typing import ClassVar, Type

import hamcrest
import hamcrest.core.base_matcher
import screenpy.actions
import screenpy.actor
import screenpy.narration.narrator
import screenpy.narration.stdout_adapter
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


if hasattr(sys, "_getframe"):
    def currentframe():
        return sys._getframe(1)
else:  # pragma: no cover

    def currentframe():
        """Return the frame object for the caller's stack frame."""
        try:
            raise Exception
        except Exception:
            return sys.exc_info()[2].tb_frame.f_back


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

    # when adding functions to this list, you must avoid those which have decorators.
    ignore_srcfiles: ClassVar[set] = set()

    def __init__(self, name, level=DEBUG):
        super().__init__(name, level)
        self.__add_level_name("TRACE", TRACE)

        self.ignore_file(logging)
        self.ignore_file(inspect.currentframe())
        self.ignore_file(contextlib)
        self.ignore_file(screenpy.narration.stdout_adapter.stdout_adapter)
        self.ignore_file(screenpy.pacing)
        self.ignore_file(screenpy.narration.narrator.Narrator)
        self.ignore_file(screenpy.actor)
        self.ignore_file(screenpy.actions.eventually)
        self.ignore_file(screenpy.actions.see)
        self.ignore_file(screenpy.actions.see_any_of)
        self.ignore_file(screenpy.actions.see_all_of)
        self.ignore_file(screenpy.resolutions.base_resolution)
        self.ignore_file(hamcrest.core.base_matcher)
        self.ignore_file(hamcrest.core.assert_that)
        self.ignore_file(hamcrest.core.core.isnot)
        return

    @staticmethod
    def __add_level_name(name: str, level: int):
        logging.addLevelName(level, name)
        setattr(logging, name, level)

    def _log(
        self,
        level: int,
        msg,
        args,
        exc_info=None,
        extra=None,
        stack_info=False,
        stacklevel=1,
    ):
        """
        Low-level logging routine which creates a LogRecord and then calls
        all the handlers of this logger to handle the record.
        """
        sinfo = None
        if self.ignore_srcfiles:
            # IronPython doesn't track Python frames, so findCaller raises an
            # exception on some versions of IronPython. We trap it here so that
            # IronPython can use logging.
            try:
                fn, lno, func, sinfo = self.findCaller(stack_info, stacklevel)
            except ValueError:  # pragma: no cover
                fn, lno, func = "(unknown file)", 0, "(unknown function)"
        else:  # pragma: no cover
            fn, lno, func = "(unknown file)", 0, "(unknown function)"

        file_line = f"{os.path.basename(fn)}:{lno}"
        if not extra:
            extra = {}
        extra["fileline"] = file_line

        if exc_info:
            if isinstance(exc_info, BaseException):
                exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
            elif not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()
        record = self.makeRecord(
            self.name, level, fn, lno, msg, args, exc_info, func, extra, sinfo
        )
        self.handle(record)

    # def findCaller2(self, stack_info=False, stacklevel=1):
    #     """
    #     Find the stack frame of the caller so that we can note the source
    #     file name, line number and function name.
    #     """
    #     # alternative way of finding the path of the module
    #     stack = inspect.stack()[2:]
    #     f = stack[0][0]
    #     info = inspect.getframeinfo(f)
    #
    #     for i in range(stacklevel, len(stack)):
    #         f = stack[i][0]
    #         info = inspect.getframeinfo(f)
    #         filename = os.path.normcase(info.filename)
    #         if filename in self.ignore_srcfiles:
    #             continue
    #         break
    #
    #     sinfo = None
    #     if stack_info:
    #         sio = io.StringIO()
    #         sio.write('Stack (most recent call last):\n')
    #         traceback.print_stack(f, file=sio)
    #         sinfo = sio.getvalue()
    #         if sinfo[-1] == '\n':
    #             sinfo = sinfo[:-1]
    #         sio.close()
    #
    #     rv = (info.filename, info.lineno, info.function, sinfo)
    #     return rv

    def findCaller(self, stack_info=False, stacklevel=1):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = currentframe()
        # On some versions of IronPython, currentframe() returns None if
        # IronPython isn't run with -X:Frames.
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
            if filename in self.ignore_srcfiles:
                f = f.f_back
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

    def ignore_file(self, path):
        p = inspect.getfile(path)
        self.ignore_srcfiles.add(p)


def create_logger(name: str = "scrnpy") -> ScreenpyLogger:
    # NOTE: do not use "screenpy" for logger name. It already exists.
    logging.setLoggerClass(ScreenpyLogger)
    # pycharm gets confused about getLogger returning ScreenpyLogger.
    # mypy also doesn't understand this since it is a dynamic call.
    logger: ScreenpyLogger = logging.getLogger(name)  # type: ignore
    logger.setLevel(DEBUG)
    logger.propagate = True
    return logger
