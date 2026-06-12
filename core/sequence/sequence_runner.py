from collections.abc import Sequence

from app_logging.log_manager import ProjectLogger, get_logger
from core.actions import (
    BaseAction,
    KeyHoldAction,
    KeyPressAction,
    KeyReleaseAction,
    WaitAction,
)
from core.input import InputController
from core.sequence.sequence_result import SequenceResult
from core.stop import StopManager
from core.timing import TimingSystem


class SequenceRunner:
    def __init__(
        self,
        timing_system: TimingSystem,
        input_controller: InputController,
        stop_manager: StopManager,
        logger: ProjectLogger | None = None,
    ) -> None:
        self._timing_system = timing_system
        self._input_controller = input_controller
        self._stop_manager = stop_manager
        self._logger = logger or get_logger()

    def run(self, actions: Sequence[BaseAction]) -> SequenceResult:
        actions_executed = 0

        for action in actions:
            if self._stop_manager.should_stop():
                return self._stop_sequence(actions_executed)

            self._run_action(action)
            actions_executed += 1

            if self._stop_manager.should_stop():
                return self._stop_sequence(actions_executed)

        self._logger.info(
            "Sequence completed with %s action(s).",
            actions_executed,
            category="sequence",
        )
        return SequenceResult(
            completed=True,
            stopped=False,
            actions_executed=actions_executed,
            message=f"Sequence completed with {actions_executed} action(s).",
        )

    def _run_action(self, action: BaseAction) -> None:
        if isinstance(action, KeyPressAction):
            self._input_controller.press_key(action.key)
            return

        if isinstance(action, KeyHoldAction):
            self._run_key_hold_action(action)
            return

        if isinstance(action, KeyReleaseAction):
            self._input_controller.release_key(action.key)
            return

        if isinstance(action, WaitAction):
            self._timing_system.wait(
                action.duration_seconds,
                should_cancel=self._stop_manager.should_stop,
            )
            return

        raise ValueError(f"Unsupported action type: {type(action).__name__}")

    def _run_key_hold_action(self, action: KeyHoldAction) -> None:
        self._input_controller.hold_key(action.key)
        timing_result = self._timing_system.wait(
            action.duration_seconds,
            should_cancel=self._stop_manager.should_stop,
        )

        if timing_result.cancelled or self._stop_manager.should_stop():
            return

        self._input_controller.release_key(action.key)

    def _stop_sequence(self, actions_executed: int) -> SequenceResult:
        stop_result = self._stop_manager.stop_and_cleanup(self._input_controller)
        self._logger.warning(
            "Sequence stopped after %s action(s).",
            actions_executed,
            category="sequence",
        )

        return SequenceResult(
            completed=False,
            stopped=True,
            actions_executed=actions_executed,
            message=f"Sequence stopped after {actions_executed} action(s).",
            stop_result=stop_result,
        )
