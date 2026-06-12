from typing import Any

from core.actions import BaseAction, KeyHoldAction, KeyPressAction, WaitAction
from profiles.profile_validator import ProfileValidationError, ProfileValidator


def build_auto1_cycle_actions(profile_data: dict[str, Any]) -> list[BaseAction]:
    try:
        ProfileValidator().validate(profile_data)
    except ProfileValidationError as error:
        raise ValueError(f"Auto1 profile is invalid: {error}") from error

    if profile_data["profile_type"] != "auto1_race":
        raise ValueError("Auto1 profile must have profile_type: auto1_race")

    keys = profile_data["keys"]
    timings = profile_data["timings"]

    return [
        WaitAction(timings["startup_delay"]),
        KeyPressAction(keys["restart_key"]),
        WaitAction(timings["wait_after_restart"]),
        KeyPressAction(keys["confirm_key"]),
        WaitAction(timings["wait_after_first_confirm"]),
        KeyPressAction(keys["confirm_key"]),
        KeyHoldAction(keys["throttle_key"], timings["race_duration"]),
        WaitAction(timings["post_cycle_delay"]),
    ]
