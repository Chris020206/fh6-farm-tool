from typing import Any

from core.actions import BaseAction, KeyPressAction, WaitAction
from profiles.profile_validator import ProfileValidationError, ProfileValidator


def build_auto2_cycle_actions(profile_data: dict[str, Any]) -> list[BaseAction]:
    keys, navigation_counts, timings = _load_auto2_profile_sections(profile_data)
    actions = _build_menu_navigation_actions(keys, navigation_counts, timings)
    actions.extend(
        [
            WaitAction(timings["wait_after_car_selection"]),
            KeyPressAction(keys["purchase_key"]),
            WaitAction(timings["menu_key_delay"]),
            KeyPressAction(keys["confirm_key"]),
            WaitAction(timings["menu_key_delay"]),
            KeyPressAction(keys["confirm_key"]),
            WaitAction(timings["menu_key_delay"]),
            KeyPressAction(keys["confirm_key"]),
            WaitAction(timings["wait_after_purchase_confirm"]),
            KeyPressAction(keys["escape_key"]),
            WaitAction(timings["menu_key_delay"]),
            KeyPressAction(keys["confirm_key"]),
            WaitAction(timings["post_cycle_delay"]),
        ]
    )
    return actions


def build_auto2_test_cycle_actions(profile_data: dict[str, Any]) -> list[BaseAction]:
    keys, navigation_counts, timings = _load_auto2_profile_sections(profile_data)
    actions = _build_menu_navigation_actions(keys, navigation_counts, timings)
    actions.extend(
        [
            WaitAction(timings["post_cycle_delay"]),
        ]
    )
    return actions


def _load_auto2_profile_sections(
    profile_data: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    try:
        ProfileValidator().validate(profile_data)
    except ProfileValidationError as error:
        raise ValueError(f"Auto2 profile is invalid: {error}") from error

    if profile_data["profile_type"] != "auto2_buy_car":
        raise ValueError("Auto2 profile must have profile_type: auto2_buy_car")

    keys = profile_data["keys"]
    navigation_counts = profile_data["navigation_counts"]
    timings = profile_data["timings"]
    return keys, navigation_counts, timings


def _build_menu_navigation_actions(
    keys: dict[str, Any],
    navigation_counts: dict[str, Any],
    timings: dict[str, Any],
) -> list[BaseAction]:
    actions: list[BaseAction] = [
        WaitAction(timings["startup_delay"]),
        KeyPressAction(keys["back_key"]),
        WaitAction(timings["menu_key_delay"]),
    ]

    actions.extend(
        _repeat_key_press(
            keys["down_key"],
            navigation_counts["manufacturer_down_presses"],
            timings["menu_key_delay"],
        )
    )
    actions.extend(
        [
            KeyPressAction(keys["confirm_key"]),
            WaitAction(timings["menu_key_delay"]),
        ]
    )
    actions.extend(
        _repeat_key_press(
            keys["right_key"],
            navigation_counts["car_right_presses"],
            timings["menu_key_delay"],
        )
    )
    actions.extend(
        [
            KeyPressAction(keys["confirm_key"]),
            WaitAction(timings["menu_key_delay"]),
            WaitAction(timings["wait_after_menu_confirm"]),
        ]
    )
    return actions


def _repeat_key_press(
    key_name: str,
    press_count: int,
    delay_seconds: float,
) -> list[BaseAction]:
    actions: list[BaseAction] = []

    for _ in range(press_count):
        actions.append(KeyPressAction(key_name))
        actions.append(WaitAction(delay_seconds))

    return actions
