from copy import deepcopy
from typing import Any

from app_logging.log_manager import ProjectLogger
from automation.auto1_race.auto1_result import Auto1LoopResult
from automation.auto1_race.auto1_runner import Auto1RaceRunner, DEFAULT_AUTO1_PROFILE_PATH
from core.input import InputController
from core.input.real_keyboard_backend import (
    RealKeyboardBackendError,
    create_real_keyboard_backend,
)
from core.input.stop_hotkey import StopHotkeyError, register_stop_hotkey
from core.stop import StopManager
from licensing import (
    EntitlementDeniedError,
    ExecutionEntitlementService,
    require_execution_entitlement,
)
from profiles import ProfileLoadError, ProfileManager


FAST_TIMINGS = {
    "startup_delay": 0.1,
    "wait_after_restart": 0.1,
    "wait_after_first_confirm": 0.1,
    "race_duration": 0.2,
    "post_cycle_delay": 0.1,
}


class Auto1ManualRunError(Exception):
    """Raised when guarded manual Auto1 real-input execution cannot start."""


def run_manual_real_input_auto1(
    cycle_count: int,
    use_fast_timings: bool,
    logger: ProjectLogger,
    profile_data: dict[str, Any] | None = None,
    stop_manager: StopManager | None = None,
    license_service: ExecutionEntitlementService | None = None,
) -> Auto1LoopResult:
    stop_manager = stop_manager or StopManager()

    try:
        require_execution_entitlement(
            "auto1",
            requested_count=cycle_count,
            license_service=license_service,
        )
        profile_data = load_manual_profile(use_fast_timings, profile_data)
        input_controller = InputController(create_real_keyboard_backend())
        stop_hotkey_registration = register_f8_stop_hotkey(stop_manager, logger)
    except (
        EntitlementDeniedError,
        ProfileLoadError,
        RealKeyboardBackendError,
        StopHotkeyError,
    ) as error:
        raise Auto1ManualRunError(str(error)) from error

    try:
        runner = Auto1RaceRunner(
            input_controller=input_controller,
            stop_manager=stop_manager,
            profile_data=profile_data,
            logger=logger,
        )
        return runner.run_cycles(cycle_count)
    except EntitlementDeniedError as error:
        raise Auto1ManualRunError(str(error)) from error
    finally:
        stop_hotkey_registration.unregister()


def load_manual_profile(
    use_fast_timings: bool,
    profile_data: dict[str, Any] | None = None,
) -> dict:
    profile_data = profile_data or ProfileManager().load_profile(DEFAULT_AUTO1_PROFILE_PATH)

    if not use_fast_timings:
        return profile_data

    fast_profile_data = deepcopy(profile_data)
    fast_profile_data["profile_id"] = "auto1_race_real_input_fast"
    fast_profile_data["profile_name"] = "Auto1 Race Real Input Fast"
    fast_profile_data["description"] = (
        "Manual real-input Auto1 profile using shortened official timings."
    )
    fast_profile_data["timings"] = FAST_TIMINGS
    return fast_profile_data


def register_f8_stop_hotkey(
    stop_manager: StopManager,
    logger: ProjectLogger,
):
    def request_stop() -> None:
        logger.warning("F8 stop hotkey triggered.", category="stop")
        stop_manager.request_stop()

    registration = register_stop_hotkey("f8", request_stop)
    logger.warning("F8 stop hotkey registered.", category="stop")
    return registration
