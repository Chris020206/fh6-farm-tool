from typing import Any

from core.actions import BaseAction, KeyPressAction, WaitAction
from profiles.profile_validator import ProfileValidationError, ProfileValidator


def build_auto3_cycle_actions(
    profile_data: dict[str, Any],
    *,
    is_first_car: bool = True,
) -> list[BaseAction]:
    if is_first_car:
        return build_auto3_first_car_exception_actions(profile_data)

    return build_auto3_get_in_next_car_actions(
        profile_data
    ) + build_auto3_unlock_perks_actions(
        profile_data,
        include_escape_to_menu=False,
    ) + build_auto3_return_and_resort_actions(profile_data)


def build_auto3_sort_setup_actions(profile_data: dict[str, Any]) -> list[BaseAction]:
    keys, navigation_counts, timings = _load_auto3_profile_sections(profile_data)

    actions: list[BaseAction] = [
        WaitAction(timings["startup_delay"]),
        KeyPressAction(keys["sort_menu_key"]),
        WaitAction(timings["menu_key_delay"]),
    ]
    actions.extend(
        _repeat_key_press(
            keys["down_key"],
            navigation_counts["sort_down_presses"],
            timings["menu_key_delay"],
        )
    )
    actions.extend(_press_with_delay(keys["confirm_key"], timings["menu_key_delay"]))
    return actions


def build_auto3_first_car_exception_actions(
    profile_data: dict[str, Any],
) -> list[BaseAction]:
    return (
        build_auto3_sort_setup_actions(profile_data)
        + build_auto3_unlock_perks_actions(profile_data)
        + build_auto3_return_and_resort_actions(profile_data)
    )


def build_auto3_first_car_exception_test_actions(
    profile_data: dict[str, Any],
) -> list[BaseAction]:
    return build_auto3_sort_setup_actions(
        profile_data
    ) + build_auto3_navigate_to_car_mastery_actions(
        profile_data,
        include_escape_to_menu=True,
    )


def build_auto3_normal_next_car_test_actions(
    profile_data: dict[str, Any],
) -> list[BaseAction]:
    return build_auto3_get_in_next_car_actions(
        profile_data
    ) + build_auto3_navigate_to_car_mastery_actions(
        profile_data,
        include_escape_to_menu=False,
    )


def build_auto3_real_input_normal_next_car_test_actions(
    profile_data: dict[str, Any],
) -> list[BaseAction]:
    return build_auto3_sort_setup_actions(
        profile_data
    ) + build_auto3_normal_next_car_test_actions(profile_data)


def build_auto3_multi_car_test_actions(
    car_count: int,
    profile_data: dict[str, Any],
) -> list[BaseAction]:
    _validate_car_count(car_count)
    from automation.auto3_skill_tree.auto3_grid_planner import (
        build_auto3_grid_movement_actions,
        movement_from_index_to_next,
    )

    actions = (
        build_auto3_first_car_exception_test_actions(profile_data)
        + build_auto3_test_mode_return_to_grid_actions(profile_data)
    )

    for previous_index in range(car_count - 1):
        movement_tokens = movement_from_index_to_next(previous_index)
        actions.extend(
            build_auto3_grid_movement_actions(movement_tokens, profile_data)
        )
        actions.extend(build_auto3_get_in_hovered_car_actions(profile_data))
        actions.extend(
            build_auto3_navigate_to_car_mastery_actions(
                profile_data,
                include_escape_to_menu=False,
            )
        )
        actions.extend(build_auto3_test_mode_return_to_grid_actions(profile_data))

    return actions


def build_auto3_multi_car_unlock_actions(
    car_count: int,
    profile_data: dict[str, Any],
) -> list[BaseAction]:
    _validate_car_count(car_count)
    from automation.auto3_skill_tree.auto3_grid_planner import (
        build_auto3_grid_movement_actions,
        movement_from_index_to_next,
    )

    actions = build_auto3_first_car_exception_actions(profile_data)

    for previous_index in range(car_count - 1):
        movement_tokens = movement_from_index_to_next(previous_index)
        actions.extend(
            build_auto3_grid_movement_actions(movement_tokens, profile_data)
        )
        actions.extend(build_auto3_get_in_hovered_car_for_unlock_actions(profile_data))
        actions.extend(
            build_auto3_post_get_in_car_mastery_navigation_actions(profile_data)
        )
        actions.extend(
            build_auto3_unlock_perks_actions(profile_data, include_navigation=False)
        )
        actions.extend(build_auto3_return_and_resort_actions(profile_data))

    return actions


def build_auto3_get_in_hovered_car_for_unlock_actions(
    profile_data: dict[str, Any],
) -> list[BaseAction]:
    keys, _, timings = _load_auto3_profile_sections(profile_data)

    return (
        _press_with_delay(keys["confirm_key"], timings["menu_key_delay"])
        + [
            KeyPressAction(keys["confirm_key"]),
            WaitAction(timings["wait_after_get_in_next_car"]),
        ]
    )


def build_auto3_get_in_hovered_car_actions(
    profile_data: dict[str, Any],
) -> list[BaseAction]:
    keys, _, timings = _load_auto3_profile_sections(profile_data)

    return (
        _press_with_delay(keys["confirm_key"], timings["menu_key_delay"])
        + _press_with_delay(keys["confirm_key"], timings["wait_after_get_in"])
    )


def build_auto3_post_get_in_car_mastery_navigation_actions(
    profile_data: dict[str, Any],
) -> list[BaseAction]:
    keys, navigation_counts, timings = _load_auto3_profile_sections(profile_data)

    actions = _press_with_delay(keys["escape_key"], timings["menu_key_delay"])
    actions.extend(
        _repeat_key_press(
            keys["up_key"],
            navigation_counts["post_get_in_up_reset_presses"],
            timings["menu_key_delay"],
        )
    )
    actions.extend(
        _repeat_key_press(
            keys["down_key"],
            navigation_counts["down_to_upgrades"],
            timings["menu_key_delay"],
        )
    )
    actions.extend(_press_with_delay(keys["confirm_key"], timings["wait_after_menu_open"]))
    actions.extend(
        _repeat_key_press(
            keys["down_key"],
            navigation_counts["down_to_car_mastery"],
            timings["menu_key_delay"],
        )
    )
    actions.extend(_press_with_delay(keys["confirm_key"], timings["wait_after_menu_open"]))
    return actions


def build_auto3_test_mode_return_to_grid_actions(
    profile_data: dict[str, Any],
) -> list[BaseAction]:
    keys, _, timings = _load_auto3_profile_sections(profile_data)

    return (
        _press_with_delay(keys["escape_key"], timings["menu_key_delay"])
        + _press_with_delay(keys["escape_key"], timings["menu_key_delay"])
        + build_auto3_return_and_resort_actions(profile_data)
    )


def _validate_car_count(car_count: int) -> None:
    if not isinstance(car_count, int):
        raise ValueError("car_count must be an integer.")

    if car_count <= 0:
        raise ValueError("car_count must be greater than 0.")


def build_auto3_get_in_next_car_actions(
    profile_data: dict[str, Any],
) -> list[BaseAction]:
    keys, _, timings = _load_auto3_profile_sections(profile_data)

    return (
        _press_with_delay(keys["down_key"], timings["menu_key_delay"])
        + _press_with_delay(keys["confirm_key"], timings["menu_key_delay"])
        + _press_with_delay(keys["confirm_key"], timings["wait_after_get_in"])
    )


def build_auto3_navigate_to_car_mastery_actions(
    profile_data: dict[str, Any],
    *,
    include_escape_to_menu: bool,
) -> list[BaseAction]:
    keys, navigation_counts, timings = _load_auto3_profile_sections(profile_data)

    actions: list[BaseAction] = []

    if include_escape_to_menu:
        actions.extend(
            _press_with_delay(
                keys["escape_key"],
                timings["menu_key_delay"],
            )
        )

    actions.extend(
        _repeat_key_press(
            keys["down_key"],
            navigation_counts["down_to_upgrades"],
            timings["menu_key_delay"],
        )
    )
    actions.extend(_press_with_delay(keys["confirm_key"], timings["wait_after_menu_open"]))
    actions.extend(
        _repeat_key_press(
            keys["down_key"],
            navigation_counts["down_to_car_mastery"],
            timings["menu_key_delay"],
        )
    )
    actions.extend(_press_with_delay(keys["confirm_key"], timings["wait_after_menu_open"]))
    return actions


def build_auto3_unlock_perks_actions(
    profile_data: dict[str, Any],
    *,
    include_escape_to_menu: bool = True,
    include_navigation: bool = True,
) -> list[BaseAction]:
    keys, _, timings = _load_auto3_profile_sections(profile_data)

    actions: list[BaseAction] = []
    if include_navigation:
        actions.extend(
            build_auto3_navigate_to_car_mastery_actions(
                profile_data,
                include_escape_to_menu=include_escape_to_menu,
            )
        )
    actions.extend(
        _build_perk_unlock_path_actions(keys, timings["skill_tree_key_delay"])
    )
    actions.extend(
        [
            WaitAction(timings["wait_after_unlock"]),
            KeyPressAction(keys["escape_key"]),
            WaitAction(timings["menu_key_delay"]),
            KeyPressAction(keys["escape_key"]),
            WaitAction(timings["menu_key_delay"]),
        ]
    )
    return actions


def build_auto3_return_and_resort_actions(
    profile_data: dict[str, Any],
) -> list[BaseAction]:
    keys, navigation_counts, timings = _load_auto3_profile_sections(profile_data)

    actions = _repeat_key_press(
        keys["up_key"],
        navigation_counts["return_up_to_my_cars"],
        timings["menu_key_delay"],
    )
    actions.extend(_press_with_delay(keys["confirm_key"], timings["menu_key_delay"]))
    actions.extend(_press_with_delay(keys["sort_menu_key"], timings["menu_key_delay"]))
    actions.extend(
        _repeat_key_press(
            keys["down_key"],
            navigation_counts["sort_down_presses"],
            timings["menu_key_delay"],
        )
    )
    actions.extend(_press_with_delay(keys["confirm_key"], timings["post_cycle_delay"]))
    return actions


def _load_auto3_profile_sections(
    profile_data: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    try:
        ProfileValidator().validate(profile_data)
    except ProfileValidationError as error:
        raise ValueError(f"Auto3 profile is invalid: {error}") from error

    if profile_data["profile_type"] != "auto3_skill_tree":
        raise ValueError("Auto3 profile must have profile_type: auto3_skill_tree")

    keys = profile_data["keys"]
    navigation_counts = profile_data["navigation_counts"]
    timings = profile_data["timings"]
    return keys, navigation_counts, timings


def _build_perk_unlock_path_actions(
    keys: dict[str, Any],
    delay_seconds: float,
) -> list[BaseAction]:
    key_sequence = [
        keys["enter_key"],
        keys["right_key"],
        keys["enter_key"],
        keys["up_key"],
        keys["enter_key"],
        keys["up_key"],
        keys["enter_key"],
        keys["up_key"],
        keys["enter_key"],
        keys["left_key"],
        keys["enter_key"],
    ]

    actions: list[BaseAction] = []
    for key_name in key_sequence:
        actions.extend(_press_with_delay(key_name, delay_seconds))

    return actions


def _repeat_key_press(
    key_name: str,
    press_count: int,
    delay_seconds: float,
) -> list[BaseAction]:
    actions: list[BaseAction] = []

    for _ in range(press_count):
        actions.extend(_press_with_delay(key_name, delay_seconds))

    return actions


def _press_with_delay(key_name: str, delay_seconds: float) -> list[BaseAction]:
    return [
        KeyPressAction(key_name),
        WaitAction(delay_seconds),
    ]
