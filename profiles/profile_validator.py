from dataclasses import dataclass
from typing import Any


REQUIRED_PROFILE_FIELDS = {
    "profile_id",
    "profile_name",
    "profile_type",
    "profile_version",
    "is_official",
    "description",
}

AUTO1_PROFILE_TYPE = "auto1_race"
AUTO2_PROFILE_TYPE = "auto2_buy_car"
AUTO3_PROFILE_TYPE = "auto3_skill_tree"
REQUIRED_AUTO1_KEY_FIELDS = {
    "restart_key",
    "confirm_key",
    "throttle_key",
}
REQUIRED_AUTO1_TIMING_FIELDS = {
    "startup_delay",
    "wait_after_restart",
    "wait_after_first_confirm",
    "race_duration",
    "post_cycle_delay",
}
REQUIRED_AUTO2_KEY_FIELDS = {
    "back_key",
    "confirm_key",
    "down_key",
    "right_key",
    "purchase_key",
    "escape_key",
}
REQUIRED_AUTO2_NAVIGATION_COUNT_FIELDS = {
    "manufacturer_down_presses",
    "car_right_presses",
}
REQUIRED_AUTO2_TIMING_FIELDS = {
    "startup_delay",
    "menu_key_delay",
    "wait_after_menu_confirm",
    "wait_after_car_selection",
    "wait_after_purchase_confirm",
    "post_cycle_delay",
}
REQUIRED_AUTO3_KEY_FIELDS = {
    "confirm_key",
    "back_key",
    "down_key",
    "enter_key",
    "escape_key",
    "left_key",
    "right_key",
    "sort_menu_key",
    "up_key",
}
REQUIRED_AUTO3_NAVIGATION_COUNT_FIELDS = {
    "sort_down_presses",
    "down_to_upgrades",
    "down_to_car_mastery",
    "post_get_in_up_reset_presses",
    "return_up_to_my_cars",
}
REQUIRED_AUTO3_TIMING_FIELDS = {
    "startup_delay",
    "menu_key_delay",
    "skill_tree_key_delay",
    "wait_after_get_in",
    "wait_after_get_in_next_car",
    "wait_after_menu_open",
    "wait_after_unlock",
    "post_cycle_delay",
}
ALLOWED_NAMED_KEYS = {
    "alt",
    "backspace",
    "ctrl",
    "delete",
    "down",
    "end",
    "enter",
    "esc",
    "home",
    "left",
    "right",
    "shift",
    "space",
    "tab",
    "up",
}


class ProfileValidationError(Exception):
    """Raised when a profile does not match the required baseline structure."""


@dataclass(frozen=True)
class ProfileValidator:
    def validate(self, profile_data: dict[str, Any]) -> None:
        missing_fields = sorted(REQUIRED_PROFILE_FIELDS - profile_data.keys())

        if missing_fields:
            raise ProfileValidationError(
                "Profile is missing required field(s): "
                + ", ".join(missing_fields)
            )

        self._validate_non_empty_text(profile_data, "profile_name")
        self._validate_non_empty_text(profile_data, "profile_type")

        if profile_data["profile_type"] == AUTO1_PROFILE_TYPE:
            self._validate_auto1_profile(profile_data)

        if profile_data["profile_type"] == AUTO2_PROFILE_TYPE:
            self._validate_auto2_profile(profile_data)

        if profile_data["profile_type"] == AUTO3_PROFILE_TYPE:
            self._validate_auto3_profile(profile_data)

    def _validate_non_empty_text(
        self,
        profile_data: dict[str, Any],
        field_name: str,
    ) -> None:
        field_value = profile_data[field_name]

        if not isinstance(field_value, str) or not field_value.strip():
            raise ProfileValidationError(
                f"Profile field must be a non-empty string: {field_name}"
            )

    def _validate_auto1_profile(self, profile_data: dict[str, Any]) -> None:
        keys = self._validate_object(profile_data, "keys")
        timings = self._validate_object(profile_data, "timings")

        self._validate_required_nested_fields(keys, REQUIRED_AUTO1_KEY_FIELDS, "keys")
        self._validate_required_nested_fields(
            timings,
            REQUIRED_AUTO1_TIMING_FIELDS,
            "timings",
        )

        for field_name in REQUIRED_AUTO1_KEY_FIELDS:
            field_value = keys[field_name]

            if not isinstance(field_value, str) or not field_value.strip():
                raise ProfileValidationError(
                    f"Auto1 key must be a non-empty string: {field_name}"
                )

            if not self._is_valid_keyboard_key_name(field_value):
                raise ProfileValidationError(
                    f"Auto1 key is not a supported keyboard key name: {field_name}"
                )

        for field_name in REQUIRED_AUTO1_TIMING_FIELDS:
            field_value = timings[field_name]

            if not isinstance(field_value, int | float) or field_value < 0:
                raise ProfileValidationError(
                    f"Auto1 timing must be a non-negative number: {field_name}"
                )

    def _validate_auto2_profile(self, profile_data: dict[str, Any]) -> None:
        keys = self._validate_object(profile_data, "keys")
        navigation_counts = self._validate_object(profile_data, "navigation_counts")
        timings = self._validate_object(profile_data, "timings")

        self._validate_required_nested_fields(keys, REQUIRED_AUTO2_KEY_FIELDS, "keys")
        self._validate_required_nested_fields(
            navigation_counts,
            REQUIRED_AUTO2_NAVIGATION_COUNT_FIELDS,
            "navigation_counts",
        )
        self._validate_required_nested_fields(
            timings,
            REQUIRED_AUTO2_TIMING_FIELDS,
            "timings",
        )

        for field_name in REQUIRED_AUTO2_KEY_FIELDS:
            self._validate_keyboard_key_field(keys, field_name, "Auto2")

        for field_name in REQUIRED_AUTO2_NAVIGATION_COUNT_FIELDS:
            field_value = navigation_counts[field_name]

            if not isinstance(field_value, int) or field_value < 0:
                raise ProfileValidationError(
                    f"Auto2 navigation count must be a non-negative integer: {field_name}"
                )

        for field_name in REQUIRED_AUTO2_TIMING_FIELDS:
            field_value = timings[field_name]

            if not isinstance(field_value, int | float) or field_value < 0:
                raise ProfileValidationError(
                    f"Auto2 timing must be a non-negative number: {field_name}"
                )

        estimated_cost_per_car = profile_data.get("estimated_cost_per_car")
        if (
            not isinstance(estimated_cost_per_car, int | float)
            or estimated_cost_per_car < 0
        ):
            raise ProfileValidationError(
                "Auto2 estimated_cost_per_car must be a non-negative number."
            )

    def _validate_auto3_profile(self, profile_data: dict[str, Any]) -> None:
        keys = self._validate_object(profile_data, "keys")
        navigation_counts = self._validate_object(profile_data, "navigation_counts")
        timings = self._validate_object(profile_data, "timings")

        self._validate_required_nested_fields(keys, REQUIRED_AUTO3_KEY_FIELDS, "keys")
        self._validate_required_nested_fields(
            navigation_counts,
            REQUIRED_AUTO3_NAVIGATION_COUNT_FIELDS,
            "navigation_counts",
        )
        self._validate_required_nested_fields(
            timings,
            REQUIRED_AUTO3_TIMING_FIELDS,
            "timings",
        )

        for field_name in REQUIRED_AUTO3_KEY_FIELDS:
            self._validate_keyboard_key_field(keys, field_name, "Auto3")

        for field_name in REQUIRED_AUTO3_NAVIGATION_COUNT_FIELDS:
            field_value = navigation_counts[field_name]

            if not isinstance(field_value, int) or field_value < 0:
                raise ProfileValidationError(
                    f"Auto3 navigation count must be a non-negative integer: {field_name}"
                )

        for field_name in REQUIRED_AUTO3_TIMING_FIELDS:
            field_value = timings[field_name]

            if not isinstance(field_value, int | float) or field_value < 0:
                raise ProfileValidationError(
                    f"Auto3 timing must be a non-negative number: {field_name}"
                )

    def _validate_keyboard_key_field(
        self,
        keys: dict[str, Any],
        field_name: str,
        profile_label: str,
    ) -> None:
        field_value = keys[field_name]

        if not isinstance(field_value, str) or not field_value.strip():
            raise ProfileValidationError(
                f"{profile_label} key must be a non-empty string: {field_name}"
            )

        if not self._is_valid_keyboard_key_name(field_value):
            raise ProfileValidationError(
                f"{profile_label} key is not a supported keyboard key name: {field_name}"
            )

    def _validate_object(
        self,
        profile_data: dict[str, Any],
        field_name: str,
    ) -> dict[str, Any]:
        field_value = profile_data.get(field_name)

        if not isinstance(field_value, dict):
            raise ProfileValidationError(
                f"Profile field must be an object: {field_name}"
            )

        return field_value

    def _validate_required_nested_fields(
        self,
        profile_section: dict[str, Any],
        required_fields: set[str],
        section_name: str,
    ) -> None:
        missing_fields = sorted(required_fields - profile_section.keys())

        if missing_fields:
            raise ProfileValidationError(
                f"Profile section {section_name} is missing required field(s): "
                + ", ".join(missing_fields)
            )

    def _is_valid_keyboard_key_name(self, key_name: str) -> bool:
        normalized_key_name = key_name.strip().lower()

        if len(normalized_key_name) == 1 and normalized_key_name.isalnum():
            return True

        return normalized_key_name in ALLOWED_NAMED_KEYS
