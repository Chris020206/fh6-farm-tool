from pathlib import Path
from typing import Any, Callable

from app_logging.log_manager import ProjectLogger, get_logger
from automation.auto3_skill_tree.auto3_result import Auto3RunResult
from automation.auto3_skill_tree.auto3_sequence import build_auto3_cycle_actions
from core.input import InputController
from core.input.input_backend import InMemoryInputBackend
from core.sequence import SequenceRunner
from core.stop import StopManager
from core.timing import TimingSystem
from profiles import ProfileManager


DEFAULT_AUTO3_PROFILE_PATH = (
    Path(__file__).resolve().parents[2]
    / "profiles"
    / "official"
    / "auto3_skill_tree_default.json"
)


class Auto3SkillTreeRunner:
    def __init__(
        self,
        timing_system: TimingSystem | None = None,
        input_controller: InputController | None = None,
        stop_manager: StopManager | None = None,
        sequence_runner: SequenceRunner | None = None,
        profile_data: dict[str, Any] | None = None,
        profile_manager: ProfileManager | None = None,
        profile_path: Path | None = None,
        action_builder: Callable[[dict[str, Any]], list] | None = None,
        logger: ProjectLogger | None = None,
    ) -> None:
        self._logger = logger or get_logger()
        self._timing_system = timing_system or TimingSystem()
        self._input_controller = input_controller or InputController(
            InMemoryInputBackend()
        )
        self._stop_manager = stop_manager or StopManager()
        self._profile_data = profile_data
        self._profile_manager = profile_manager or ProfileManager()
        self._profile_path = profile_path or DEFAULT_AUTO3_PROFILE_PATH
        self._action_builder = action_builder or build_auto3_cycle_actions
        self._sequence_runner = sequence_runner or SequenceRunner(
            self._timing_system,
            self._input_controller,
            self._stop_manager,
            self._logger,
        )

    def run_one_cycle(self) -> Auto3RunResult:
        self._logger.info("Auto3 one-cycle run started.", category="sequence")

        try:
            profile_data = self._profile_data or self._profile_manager.load_profile(
                self._profile_path
            )
            actions = self._action_builder(profile_data)
            sequence_result = self._sequence_runner.run(actions)
        except Exception as error:
            cleanup_result = self._input_controller.release_all_keys()
            message = f"Auto3 one-cycle run failed: {error}"
            self._logger.error(message, category="error")

            return Auto3RunResult(
                status="failed",
                message=message,
                cleanup_result=cleanup_result,
            )

        cleanup_result = self._input_controller.release_all_keys()

        if sequence_result.stopped:
            message = f"Auto3 one-cycle run stopped: {sequence_result.message}"
            self._logger.warning(message, category="sequence")

            return Auto3RunResult(
                status="stopped",
                message=message,
                sequence_result=sequence_result,
                cleanup_result=cleanup_result,
            )

        message = f"Auto3 one-cycle run completed: {sequence_result.message}"
        self._logger.info(message, category="sequence")

        return Auto3RunResult(
            status="completed",
            message=message,
            sequence_result=sequence_result,
            cleanup_result=cleanup_result,
        )


def run_auto3_cycle(
    timing_system: TimingSystem | None = None,
    input_controller: InputController | None = None,
    stop_manager: StopManager | None = None,
    sequence_runner: SequenceRunner | None = None,
    profile_data: dict[str, Any] | None = None,
    profile_manager: ProfileManager | None = None,
    profile_path: Path | None = None,
    action_builder: Callable[[dict[str, Any]], list] | None = None,
    logger: ProjectLogger | None = None,
) -> Auto3RunResult:
    runner = Auto3SkillTreeRunner(
        timing_system=timing_system,
        input_controller=input_controller,
        stop_manager=stop_manager,
        sequence_runner=sequence_runner,
        profile_data=profile_data,
        profile_manager=profile_manager,
        profile_path=profile_path,
        action_builder=action_builder,
        logger=logger,
    )
    return runner.run_one_cycle()
