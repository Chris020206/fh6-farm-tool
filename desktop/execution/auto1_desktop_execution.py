"""Desktop adapter for guarded Auto1 execution."""

from copy import deepcopy
from pathlib import Path
import threading

from desktop.execution.execution_messages import (
    completion_state_id_for_auto1_status,
    summarize_auto1_ui_execution_error,
)

AUTO1_RACE_DURATION_MIN_SECONDS = 5.0
AUTO1_RACE_DURATION_MAX_SECONDS = 180.0
AUTO1_RACE_DURATION_EXECUTION_BUFFER_SECONDS = 5.0
AUTO1_LOOP_COUNT_MIN = 1
AUTO1_LOOP_COUNT_MAX = 25
DEFAULT_AUTO1_PROFILE_PATH = (
    Path(__file__).resolve().parents[2]
    / "profiles"
    / "official"
    / "auto1_race_default.json"
)


def start_auto1_ui_execution(
    companion_state: dict[str, str],
    parent,
    timer_type,
    on_result,
    stop_manager,
) -> None:
    execution_state = {
        "done": False,
        "state_id": "refused",
        "message": "Auto1 execution did not start.",
    }
    poll_timer = timer_type(parent)
    poll_timer.setInterval(250)

    def worker() -> None:
        from app_logging.log_manager import configure_logging

        logger = configure_logging()
        logger.warning(
            "UI-triggered Auto1 execution attempt starting. cycles=%s profile=%s",
            companion_state.get("requested_cycles", "1"),
            companion_state.get("profile_id", "default"),
            category="sequence",
        )
        try:
            from automation.auto1_race.manual_real_input_runner import (
                run_manual_real_input_auto1,
            )

            result = run_manual_real_input_auto1(
                cycle_count=parse_auto1_loop_count(
                    companion_state.get("requested_cycles")
                ),
                use_fast_timings=False,
                logger=logger,
                profile_data=build_auto1_ui_execution_profile(companion_state),
                stop_manager=stop_manager,
            )
            execution_state["state_id"] = completion_state_id_for_auto1_status(
                result.status
            )
            execution_state["message"] = (
                f"{result.message} Completed cycles: "
                f"{result.completed_cycles}/{result.requested_cycles}."
            )
            logger.warning(
                "UI-triggered Auto1 execution returned status=%s completed_cycles=%s/%s.",
                result.status,
                result.completed_cycles,
                result.requested_cycles,
                category="sequence",
            )
        except Exception as error:
            execution_state["state_id"] = "refused"
            execution_state["message"] = summarize_auto1_ui_execution_error(error)
            logger.error(
                "UI-triggered Auto1 execution failed closed: %s",
                execution_state["message"],
                category="error",
            )
        finally:
            execution_state["done"] = True

    def poll_for_result() -> None:
        if not execution_state["done"]:
            return

        poll_timer.stop()
        on_result(
            execution_state["state_id"],
            companion_state,
            execution_state["message"],
        )

    poll_timer.timeout.connect(poll_for_result)
    threading.Thread(target=worker, daemon=True).start()
    poll_timer.start()


def build_auto1_ui_execution_profile(companion_state: dict[str, str]) -> dict:
    from profiles import ProfileManager

    displayed_race_duration = parse_auto1_race_duration_override(
        companion_state.get("race_duration_seconds")
    )
    profile_data = ProfileManager().load_profile(DEFAULT_AUTO1_PROFILE_PATH)
    execution_profile = deepcopy(profile_data)
    execution_profile["timings"] = dict(profile_data["timings"])
    execution_profile["timings"]["race_duration"] = auto1_execution_race_duration(
        displayed_race_duration
    )
    return execution_profile


def parse_auto1_race_duration_override(raw_value: str | None) -> float:
    if raw_value is None:
        raise ValueError("Race drive duration was not provided.")

    try:
        race_duration = float(raw_value)
    except (TypeError, ValueError) as error:
        raise ValueError("Race drive duration must be a number.") from error

    if not (
        AUTO1_RACE_DURATION_MIN_SECONDS
        <= race_duration
        <= AUTO1_RACE_DURATION_MAX_SECONDS
    ):
        raise ValueError(
            "Race drive duration must be between "
            f"{AUTO1_RACE_DURATION_MIN_SECONDS:.0f} and "
            f"{AUTO1_RACE_DURATION_MAX_SECONDS:.0f} seconds."
        )

    return race_duration


def parse_auto1_loop_count(raw_value: str | None) -> int:
    try:
        loop_count = int(raw_value or str(AUTO1_LOOP_COUNT_MIN))
    except (TypeError, ValueError) as error:
        raise ValueError("Auto1 loop count must be an integer.") from error

    if not AUTO1_LOOP_COUNT_MIN <= loop_count <= AUTO1_LOOP_COUNT_MAX:
        raise ValueError(
            f"Auto1 loop count must be between {AUTO1_LOOP_COUNT_MIN} and {AUTO1_LOOP_COUNT_MAX}."
        )

    return loop_count


def auto1_execution_race_duration(displayed_race_duration: float) -> float:
    return displayed_race_duration + AUTO1_RACE_DURATION_EXECUTION_BUFFER_SECONDS


def load_auto1_default_race_duration() -> float:
    from profiles import ProfileManager

    profile_data = ProfileManager().load_profile(DEFAULT_AUTO1_PROFILE_PATH)
    return float(profile_data["timings"]["race_duration"])

