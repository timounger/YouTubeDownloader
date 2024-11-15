"""!
********************************************************************************
@file   colored_log.py
@brief  Logging formatter for colored log in terminal.
********************************************************************************
"""

import logging
from logging import LogRecord
from typing import Optional, Any
from types import TracebackType
from colorama import just_fix_windows_console
just_fix_windows_console()

# Possible Log Level:
# CRITICAL = 50
# FATAL = CRITICAL
# ERROR = 40
# WARNING = 30
# WARN = WARNING
# INFO = 20
# DEBUG = 10
# NOTSET = 0

S_LOG_MSG_FORMAT_WO_LINENO_WO_THREADS = "%(asctime)s [%(name)s][%(levelname)s] %(message)s"
S_LOG_MSG_FORMAT_WO_LINENO_W_THREADS = "%(asctime)s [%(name)s][%(threadName)s][%(levelname)s] %(message)s"
S_LOG_MSG_FORMAT_W_LINENO_WO_THREADS = "%(asctime)s [%(name)s:%(lineno)d][%(levelname)s] %(message)s"
S_LOG_MSG_FORMAT_W_LINENO_W_THREADS = "%(asctime)s [%(name)s:%(lineno)d][%(threadName)s][%(levelname)s] %(message)s"
S_LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_format(line_no: bool = False, threads: bool = False) -> str:
    """!
    @brief Get the configurable log format string
    @param line_no : include line number in log string
    @param threads : include thread name in log string
    @return log format string
    """
    if not line_no and not threads:
        msg_format = S_LOG_MSG_FORMAT_WO_LINENO_WO_THREADS
    elif not line_no and threads:
        msg_format = S_LOG_MSG_FORMAT_WO_LINENO_W_THREADS
    elif line_no and not threads:
        msg_format = S_LOG_MSG_FORMAT_W_LINENO_WO_THREADS
    elif line_no and threads:
        msg_format = S_LOG_MSG_FORMAT_W_LINENO_W_THREADS
    else:
        raise ValueError("No valid format found")
    return msg_format


def init_console_logging(level: int, threads: bool = False) -> None:
    """!
    @brief Initializes logging for console output.
           Line numbers are active in DEBUG level or lower.
    @param level : root log level
    @param threads : include thread names in log strings
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    stream_handler = logging.StreamHandler()
    line_no = bool(level == logging.DEBUG)
    date_format = S_LOG_DATE_FORMAT if (level != logging.DEBUG) else None
    stream_handler.setFormatter(ColorFormatter(line_no=line_no, threads=threads, data_format=date_format))
    root_logger.handlers.clear()
    root_logger.addHandler(stream_handler)


class ColorFormatter(logging.Formatter):
    """!
    @brief Logging formatter that colors logging messages depending on their level
    @param fmt : [optional] overwrite format with a complete custom log format -> ignores all other parameters
    @param line_no : [optional] include line number in log format string
    @param threads : [optional] include thread names in log format string
    @param data_format : [optional] date format
    """
    fg_grey = "\033[90m"
    fg_yellow = "\033[33m"
    fg_red = "\033[31m"
    bg_red = "\033[41m"
    reset = "\033[0m"

    def __init__(self, fmt: Optional[str] = None, line_no: bool = True, threads: bool = False, data_format: Optional[str] = None, **kwargs: Any) -> None:
        super().__init__(fmt, **kwargs)
        msg_format = fmt if fmt else get_format(line_no=line_no, threads=threads)
        self.d_formats = {
            logging.DEBUG: self.fg_grey + msg_format + self.reset,
            logging.INFO: self.reset + msg_format,
            logging.WARNING: self.fg_yellow + msg_format + self.reset,
            logging.ERROR: self.fg_red + msg_format + self.reset,
            logging.CRITICAL: self.bg_red + msg_format + self.reset
        }
        self.data_format = data_format

    def format(self, record: LogRecord) -> str:
        """!
        @brief Overwrite format method of logging.Formatter to use colors formatting
        @param record : log record
        @return formatted log record
        """
        log_fmt = self.d_formats.get(record.levelno)
        formatter = logging.Formatter(fmt=log_fmt, datefmt=self.data_format)
        return formatter.format(record)

    def formatException(self, ei: tuple[type[BaseException], BaseException, TracebackType | None] | tuple[None, None, None]) -> str:
        """!
        @brief Overwrite formatException method of logging. Formatter to use critical color formatting
        @param ei : exception info
        @return formatted exception log record
        """
        log_fmt = self.d_formats.get(logging.CRITICAL)
        formatter = logging.Formatter(log_fmt, datefmt=self.data_format)
        record = super().formatException(ei)
        return formatter.format(record)  # type: ignore


if __name__ == "__main__":
    log = logging.getLogger(__name__)
    init_console_logging(logging.DEBUG)
    log.debug("Debug")
    log.info("Info")
    log.warning("Warning")
    log.error("Error")
    log.critical("Critical")
