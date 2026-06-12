import unittest

from automation.auto2_buy_car.auto2_runner import DEFAULT_AUTO2_PROFILE_PATH
from automation.auto2_buy_car.auto2_sequence import (
    build_auto2_cycle_actions,
    build_auto2_test_cycle_actions,
)
from core.actions import KeyPressAction, WaitAction
from profiles import ProfileManager


class Auto2NavigationCountsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.profile_data = ProfileManager().load_profile(DEFAULT_AUTO2_PROFILE_PATH)

    def test_test_mode_sequence_uses_profile_navigation_counts(self) -> None:
        actions = build_auto2_test_cycle_actions(self.profile_data)

        self.assertEqual(18, _count_key_presses(actions, "down"))
        self.assertEqual(3, _count_key_presses(actions, "right"))

    def test_full_sequence_uses_profile_navigation_counts(self) -> None:
        actions = build_auto2_cycle_actions(self.profile_data)

        self.assertEqual(18, _count_key_presses(actions, "down"))
        self.assertEqual(3, _count_key_presses(actions, "right"))

    def test_repeated_navigation_key_presses_have_menu_delays(self) -> None:
        actions = build_auto2_test_cycle_actions(self.profile_data)
        menu_key_delay = self.profile_data["timings"]["menu_key_delay"]

        for index, action in enumerate(actions[:-1]):
            if isinstance(action, KeyPressAction) and action.key in {"down", "right"}:
                next_action = actions[index + 1]
                self.assertIsInstance(next_action, WaitAction)
                self.assertEqual(menu_key_delay, next_action.duration_seconds)

    def test_full_sequence_includes_purchase_and_reset_path(self) -> None:
        actions = build_auto2_cycle_actions(self.profile_data)
        keys = self.profile_data["keys"]
        timings = self.profile_data["timings"]
        purchase_index = _find_key_press_index(actions, keys["purchase_key"])

        self.assertIsNotNone(purchase_index)
        wait_before_purchase = actions[purchase_index - 1]

        self.assertIsInstance(wait_before_purchase, WaitAction)
        self.assertEqual(
            timings["wait_after_car_selection"],
            wait_before_purchase.duration_seconds,
        )

        path_after_purchase = actions[purchase_index:]
        self.assertEqual(keys["purchase_key"], path_after_purchase[0].key)
        self.assertEqual(keys["confirm_key"], path_after_purchase[2].key)
        self.assertEqual(keys["confirm_key"], path_after_purchase[4].key)
        self.assertEqual(keys["confirm_key"], path_after_purchase[6].key)
        self.assertEqual(
            timings["wait_after_purchase_confirm"],
            path_after_purchase[7].duration_seconds,
        )
        self.assertEqual(keys["escape_key"], path_after_purchase[8].key)
        self.assertEqual(keys["confirm_key"], path_after_purchase[10].key)
        self.assertEqual(timings["post_cycle_delay"], path_after_purchase[11].duration_seconds)

    def test_test_mode_excludes_purchase_and_reset_path(self) -> None:
        actions = build_auto2_test_cycle_actions(self.profile_data)
        keys = self.profile_data["keys"]

        self.assertEqual(0, _count_key_presses(actions, keys["purchase_key"]))
        self.assertEqual(0, _count_key_presses(actions, keys["escape_key"]))
        self.assertEqual(2, _count_key_presses(actions, keys["confirm_key"]))
        self.assertFalse(
            _has_wait_duration(
                actions,
                self.profile_data["timings"]["wait_after_car_selection"],
            )
        )

    def test_official_profile_wait_after_purchase_confirm_is_thirteen_seconds(self) -> None:
        self.assertEqual(
            13.0,
            self.profile_data["timings"]["wait_after_purchase_confirm"],
        )


def _count_key_presses(actions: list, key_name: str) -> int:
    return sum(
        1
        for action in actions
        if isinstance(action, KeyPressAction) and action.key == key_name
    )


def _find_key_press_index(actions: list, key_name: str) -> int | None:
    for index, action in enumerate(actions):
        if isinstance(action, KeyPressAction) and action.key == key_name:
            return index

    return None


def _has_wait_duration(actions: list, duration_seconds: float) -> bool:
    return any(
        isinstance(action, WaitAction) and action.duration_seconds == duration_seconds
        for action in actions
    )


if __name__ == "__main__":
    unittest.main()
