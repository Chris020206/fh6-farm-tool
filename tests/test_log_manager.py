from io import StringIO
import unittest
from unittest.mock import patch

from app_logging.log_manager import ProjectLogger


class BrokenStream:
    def write(self, _message: str) -> None:
        raise ValueError("stream unavailable")

    def flush(self) -> None:
        raise ValueError("stream unavailable")


class TestProjectLogger(unittest.TestCase):
    def test_writes_to_available_stream(self) -> None:
        stream = StringIO()
        logger = ProjectLogger("test_logger", stream=stream)

        logger.info("hello %s", "world", category="startup")

        output = stream.getvalue()
        self.assertIn("INFO | test_logger | startup | hello world", output)

    def test_noops_when_default_stream_is_none(self) -> None:
        with patch("sys.stderr", None):
            logger = ProjectLogger("test_logger")

        logger.info("safe without stderr")

    def test_noops_when_stream_becomes_none(self) -> None:
        logger = ProjectLogger("test_logger", stream=StringIO())
        logger.stream = None

        logger.info("safe without stream")

    def test_noops_when_stream_is_unavailable(self) -> None:
        logger = ProjectLogger("test_logger", stream=BrokenStream())

        logger.info("safe with broken stream")


if __name__ == "__main__":
    unittest.main()
