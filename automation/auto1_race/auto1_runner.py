from pathlib import Path
from typing import Any

from app_logging.log_manager import ProjectLogger, get_logger
from automation.auto1_race.auto1_result import Auto1LoopResult, Auto1RunResult
from automation.auto1_race.auto1_sequence import build_auto1_cycle_actions
from core.input import InputController
from core.sequence import SequenceRunner
from core.stop import StopManager
from core.timing import TimingSystem
from profiles import ProfileManager


DEFAULT_AUTO1_PROFILE_PATH = (
    Path(__file__).resolve().parents[2]
    / "profiles"
    / "official"
    / "auto1_race_default.json"
)


class Auto1RaceRunner:
    def __init__(
        self,
        timing_system: TimingSystem | None = None,
        input_controller: InputController | None = None,
        stop_manager: StopManager | None = None,
        sequence_runner: SequenceRunner | None = None,
        profile_data: dict[str, Any] | None = None,
        profile_manager: ProfileManager | None = None,
        profile_path: Path | None = None,
        logger: ProjectLogger | None = None,
    ) -> None:
        self._logger = logger or get_logger()
        self._timing_system = timing_system or TimingSystem()
        self._input_controller = input_controller or InputController()
        self._stop_manager = stop_manager or StopManager()
        self._profile_data = profile_data
        self._profile_manager = profile_manager or ProfileManager()
        self._profile_path = profile_path or DEFAULT_AUTO1_PROFILE_PATH
        self._sequence_runner = sequence_runner or SequenceRunner(
            self._timing_system,
            self._input_controller,
            self._stop_manager,
            self._logger,
        )

    def run_one_cycle(self) -> Auto1RunResult:
        self._logger.info("Auto1 one-cycle run started.", category="sequence")

        try:
            profile_data = self._profile_data or self._profile_manager.load_profile(
                self._profile_path
            )
            actions = build_auto1_cycle_actions(profile_data)
            sequence_result = self._sequence_runner.run(actions)
        except Exception as error:
            cleanup_result = self._input_controller.release_all_keys()
            message = f"Auto1 one-cycle run failed: {error}"
            self._logger.error(message, category="error")

            return Auto1RunResult(
                status="failed",
                message=message,
                cleanup_result=cleanup_result,
            )

        cleanup_result = self._input_controller.release_all_keys()

        if sequence_result.stopped:
            message = f"Auto1 one-cycle run stopped: {sequence_result.message}"
            self._logger.warning(message, category="sequence")

            return Auto1RunResult(
                status="stopped",
                message=message,
                sequence_result=sequence_result,
                cleanup_result=cleanup_result,
            )

        message = f"Auto1 one-cycle run completed: {sequence_result.message}"
        self._logger.info(message, category="sequence")

        return Auto1RunResult(
            status="completed",
            message=message,
            sequence_result=sequence_result,
            cleanup_result=cleanup_result,
        )

    def run_cycles(self, cycle_count: int) -> Auto1LoopResult:
        try:
            self._validate_cycle_count(cycle_count)
        except ValueError as error:
            cleanup_result = self._input_controller.release_all_keys()
            message = f"Auto1 loop failed: {error}"
            self._logger.error(message, category="error")

            return Auto1LoopResult(
                status="failed",
                requested_cycles=0,
                completed_cycles=0,
                message=message,
                cleanup_result=cleanup_result,
            )

        completed_cycles = 0
        last_cycle_result: Auto1RunResult | None = None

        for cycle_number in range(1, cycle_count + 1):
            if self._stop_manager.should_stop():
                cleanup_result = self._input_controller.release_all_keys()
                message = (
                    "Auto1 loop stopped before cycle "
                    f"{cycle_number}: stop requested."
                )
                self._logger.warning(message, category="sequence")

                return Auto1LoopResult(
                    status="stopped",
                    requested_cycles=cycle_count,
                    completed_cycles=completed_cycles,
                    message=message,
                    last_cycle_result=last_cycle_result,
                    cleanup_result=cleanup_result,
                )

            self._logger.info(
                "Auto1 cycle %s of %s started.",
                cycle_number,
                cycle_count,
                category="sequence",
            )
            last_cycle_result = self.run_one_cycle()

            if last_cycle_result.completed:
                completed_cycles += 1
                self._logger.info(
                    "Auto1 cycle %s of %s completed.",
                    cycle_number,
                    cycle_count,
                    category="sequence",
                )
                continue

            cleanup_result = self._input_controller.release_all_keys()

            if last_cycle_result.stopped:
                message = f"Auto1 loop stopped after {completed_cycles} cycle(s)."
                self._logger.warning(message, category="sequence")

                return Auto1LoopResult(
                    status="stopped",
                    requested_cycles=cycle_count,
                    completed_cycles=completed_cycles,
                    message=message,
                    last_cycle_result=last_cycle_result,
                    cleanup_result=cleanup_result,
                )

            message = f"Auto1 loop failed after {completed_cycles} cycle(s)."
            self._logger.error(message, category="error")

            return Auto1LoopResult(
                status="failed",
                requested_cycles=cycle_count,
                completed_cycles=completed_cycles,
                message=message,
                last_cycle_result=last_cycle_result,
                cleanup_result=cleanup_result,
            )

        cleanup_result = self._input_controller.release_all_keys()
        message = f"Auto1 loop completed {completed_cycles} cycle(s)."
        self._logger.info(message, category="sequence")

        return Auto1LoopResult(
            status="completed",
            requested_cycles=cycle_count,
            completed_cycles=completed_cycles,
            message=message,
            last_cycle_result=last_cycle_result,
            cleanup_result=cleanup_result,
        )

    def _validate_cycle_count(self, cycle_count: int) -> None:
        if not isinstance(cycle_count, int):
            raise ValueError("Cycle count must be an integer.")

        if cycle_count <= 0:
            raise ValueError("Cycle count must be greater than 0.")


def run_auto1_cycle(
    timing_system: TimingSystem | None = None,
    input_controller: InputController | None = None,
    stop_manager: StopManager | None = None,
    sequence_runner: SequenceRunner | None = None,
    profile_data: dict[str, Any] | None = None,
    profile_manager: ProfileManager | None = None,
    profile_path: Path | None = None,
    logger: ProjectLogger | None = None,
) -> Auto1RunResult:
    runner = Auto1RaceRunner(
        timing_system=timing_system,
        input_controller=input_controller,
        stop_manager=stop_manager,
        sequence_runner=sequence_runner,
        profile_data=profile_data,
        profile_manager=profile_manager,
        profile_path=profile_path,
        logger=logger,
    )
    return runner.run_one_cycle()


def run_auto1_cycles(
    cycle_count: int,
    timing_system: TimingSystem | None = None,
    input_controller: InputController | None = None,
    stop_manager: StopManager | None = None,
    sequence_runner: SequenceRunner | None = None,
    profile_data: dict[str, Any] | None = None,
    profile_manager: ProfileManager | None = None,
    profile_path: Path | None = None,
    logger: ProjectLogger | None = None,
) -> Auto1LoopResult:
    runner = Auto1RaceRunner(
        timing_system=timing_system,
        input_controller=input_controller,
        stop_manager=stop_manager,
        sequence_runner=sequence_runner,
        profile_data=profile_data,
        profile_manager=profile_manager,
        profile_path=profile_path,
        logger=logger,
    )
    return runner.run_cycles(cycle_count)
