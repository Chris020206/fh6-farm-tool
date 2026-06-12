from datetime import datetime
from typing import TextIO
import sys


LOGGER_NAME = "fh6_farm_tool"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_CATEGORY = "startup"
CATEGORIES = {
    "startup",
    "config",
    "timing",
    "input",
    "stop",
    "sequence",
    "state",
    "profile",
    "error",
}
LEVELS = {
    "INFO": 20,
    "WARNING": 30,
    "ERROR": 40,
}


def _parse_level(level: str) -> int:
    return LEVELS.get(level.upper(), LEVELS["INFO"])


class ProjectLogger:
    def __init__(self, name: str, level: str = "INFO", stream: TextIO | None = None):
        self.name = name
        self.level = _parse_level(level)
        self.stream = stream or sys.stderr

    def set_level(self, level: str) -> None:
        self.level = _parse_level(level)

    def info(self, message: str, *args: object, category: str = DEFAULT_CATEGORY) -> None:
        self._log("INFO", category, message, *args)

    def warning(
        self,
        message: str,
        *args: object,
        category: str = DEFAULT_CATEGORY,
    ) -> None:
        self._log("WARNING", category, message, *args)

    def error(self, message: str, *args: object, category: str = "error") -> None:
        self._log("ERROR", category, message, *args)

    def event(
        self,
        category: str,
        message: str,
        *args: object,
        level: str = "INFO",
    ) -> None:
        self._log(level.upper(), category, message, *args)

    def _log(self, level: str, category: str, message: str, *args: object) -> None:
        parsed_level = _parse_level(level)
        if parsed_level < self.level:
            return

        normalized_category = _parse_category(category)
        formatted_message = message % args if args else message
        timestamp = datetime.now().strftime(DATE_FORMAT)
        self.stream.write(
            f"{timestamp} | {level} | {self.name} | "
            f"{normalized_category} | {formatted_message}\n"
        )
        self.stream.flush()


_LOGGER = ProjectLogger(LOGGER_NAME)


def configure_logging(level: str = "INFO") -> ProjectLogger:
    _LOGGER.set_level(level)
    return _LOGGER


def get_logger() -> ProjectLogger:
    return _LOGGER


def _parse_category(category: str) -> str:
    normalized_category = category.strip().lower()

    if normalized_category in CATEGORIES:
        return normalized_category

    return "error"
