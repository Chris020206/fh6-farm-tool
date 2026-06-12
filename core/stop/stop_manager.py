from app_logging.log_manager import get_logger
from core.input.input_controller import InputController
from core.stop.stop_result import StopResult


class StopManager:
    def __init__(self) -> None:
        self._stop_requested = False
        self._logger = get_logger()

    def request_stop(self) -> StopResult:
        self._stop_requested = True
        self._logger.warning("Stop requested.", category="stop")

        return StopResult(
            stop_requested=True,
            cleanup_result=None,
            message="Stop requested.",
        )

    def clear_stop(self) -> StopResult:
        self._stop_requested = False
        self._logger.info("Stop state cleared.", category="stop")

        return StopResult(
            stop_requested=False,
            cleanup_result=None,
            message="Stop state cleared.",
        )

    def should_stop(self) -> bool:
        return self._stop_requested

    def stop_and_cleanup(self, input_controller: InputController) -> StopResult:
        self._stop_requested = True
        cleanup_result = input_controller.release_all_keys()
        self._logger.warning(
            "Stop requested and input cleanup completed.",
            category="stop",
        )

        return StopResult(
            stop_requested=True,
            cleanup_result=cleanup_result,
            message="Stop requested and held keys released.",
        )
