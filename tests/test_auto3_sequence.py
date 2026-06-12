import copy
import json
import unittest
from pathlib import Path

from automation.auto3_skill_tree.auto3_runner import run_auto3_cycle
from automation.auto3_skill_tree.auto3_sequence import (
    build_auto3_cycle_actions,
    build_auto3_first_car_exception_actions,
    build_auto3_first_car_exception_test_actions,
    build_auto3_get_in_hovered_car_actions,
    build_auto3_get_in_next_car_actions,
    build_auto3_multi_car_test_actions,
    build_auto3_multi_car_unlock_actions,
    build_auto3_normal_next_car_test_actions,
    build_auto3_post_get_in_car_mastery_navigation_actions,
    build_auto3_real_input_normal_next_car_test_actions,
    build_auto3_return_and_resort_actions,
    build_auto3_test_mode_return_to_grid_actions,
    build_auto3_unlock_perks_actions,
)
from core.actions import KeyPressAction, WaitAction
from core.input import InputController
from core.input.input_backend import InMemoryInputBackend
from core.stop import StopManager


PROFILE_PATH = Path("profiles/official/auto3_skill_tree_default.json")


def _key_presses(actions) -> list[str]:
    return [
        action.key
        for action in actions
        if isinstance(action, KeyPressAction)
    ]


class Auto3SequenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.profile_data = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))

    def test_first_car_exception_excludes_get_in_next_car_prefix(self) -> None:
        actions = build_auto3_first_car_exception_actions(self.profile_data)
        key_presses = _key_presses(actions)

        self.assertEqual(key_presses[0], "x")
        self.assertNotEqual(key_presses[:3], ["down", "enter", "enter"])

    def test_normal_next_car_path_includes_get_in_next_car_prefix(self) -> None:
        actions = build_auto3_cycle_actions(self.profile_data, is_first_car=False)
        key_presses = _key_presses(actions)

        self.assertEqual(key_presses[:3], ["down", "enter", "enter"])

    def test_get_in_next_car_sequence_matches_locked_flow(self) -> None:
        actions = build_auto3_get_in_next_car_actions(self.profile_data)

        self.assertEqual(_key_presses(actions), ["down", "enter", "enter"])

    def test_get_in_hovered_car_sequence_excludes_movement(self) -> None:
        actions = build_auto3_get_in_hovered_car_actions(self.profile_data)

        self.assertEqual(_key_presses(actions), ["enter", "enter"])

    def test_post_get_in_navigation_uses_transition_recovery_path(self) -> None:
        actions = build_auto3_post_get_in_car_mastery_navigation_actions(
            self.profile_data
        )

        self.assertEqual(
            _key_presses(actions),
            ["esc"] + ["up"] * 6 + ["down", "enter"] + ["down"] * 7 + ["enter"],
        )

    def test_unlock_sequence_includes_perk_confirmations_in_locked_order(self) -> None:
        actions = build_auto3_unlock_perks_actions(self.profile_data)
        key_presses = _key_presses(actions)
        perk_path = _perk_path()

        self.assertIn(perk_path, _windows(key_presses, len(perk_path)))
        self.assertEqual(perk_path.count("enter"), 6)

    def test_unlock_path_uses_skill_tree_key_delay(self) -> None:
        actions = build_auto3_unlock_perks_actions(self.profile_data)
        perk_path = _perk_path()
        perk_start_index = _find_key_path_start(actions, perk_path)

        for action_index in range(perk_start_index, perk_start_index + len(perk_path) * 2, 2):
            self.assertIsInstance(actions[action_index], KeyPressAction)
            self.assertIsInstance(actions[action_index + 1], WaitAction)
            self.assertEqual(actions[action_index + 1].duration_seconds, 1.5)

    def test_menu_navigation_still_uses_menu_key_delay(self) -> None:
        actions = build_auto3_first_car_exception_test_actions(self.profile_data)
        first_down_index = _find_key_path_start(actions, ["esc", "down", "enter"])

        self.assertIsInstance(actions[first_down_index + 1], WaitAction)
        self.assertEqual(actions[first_down_index + 1].duration_seconds, 1.0)
        self.assertIsInstance(actions[first_down_index + 3], WaitAction)
        self.assertEqual(actions[first_down_index + 3].duration_seconds, 1.0)

    def test_return_and_resort_sequence_matches_locked_flow(self) -> None:
        actions = build_auto3_return_and_resort_actions(self.profile_data)

        self.assertEqual(
            _key_presses(actions),
            ["up"] * 7 + ["enter", "x"] + ["down"] * 6 + ["enter"],
        )

    def test_invalid_profile_fails_clearly(self) -> None:
        profile_data = copy.deepcopy(self.profile_data)
        del profile_data["timings"]["wait_after_unlock"]

        with self.assertRaisesRegex(ValueError, "Auto3 profile is invalid"):
            build_auto3_cycle_actions(profile_data)

    def test_missing_later_car_get_in_timing_fails_clearly(self) -> None:
        profile_data = copy.deepcopy(self.profile_data)
        del profile_data["timings"]["wait_after_get_in_next_car"]

        with self.assertRaisesRegex(ValueError, "Auto3 profile is invalid"):
            build_auto3_multi_car_unlock_actions(2, profile_data)

    def test_full_first_car_sequence_includes_perk_unlock_actions(self) -> None:
        actions = build_auto3_first_car_exception_actions(self.profile_data)
        key_presses = _key_presses(actions)
        perk_path = _perk_path()

        self.assertIn(perk_path, _windows(key_presses, len(perk_path)))

    def test_test_first_car_sequence_excludes_perk_unlock_actions(self) -> None:
        actions = build_auto3_first_car_exception_test_actions(self.profile_data)
        key_presses = _key_presses(actions)
        perk_path = _perk_path()

        self.assertEqual(key_presses[0], "x")
        self.assertIn(_first_car_menu_navigation(), _windows(key_presses, 11))
        self.assertNotIn(perk_path, _windows(key_presses, len(perk_path)))
        self.assertNotIn(1.5, _wait_durations(actions))

    def test_first_car_test_uses_corrected_menu_navigation_counts(self) -> None:
        actions = build_auto3_first_car_exception_test_actions(self.profile_data)
        key_presses = _key_presses(actions)

        self.assertIn(_first_car_menu_navigation(), _windows(key_presses, 11))

    def test_full_normal_next_car_sequence_includes_get_in_and_perk_unlock_actions(
        self,
    ) -> None:
        actions = build_auto3_cycle_actions(self.profile_data, is_first_car=False)
        key_presses = _key_presses(actions)
        perk_path = _perk_path()

        self.assertEqual(key_presses[:3], ["down", "enter", "enter"])
        self.assertIn(perk_path, _windows(key_presses, len(perk_path)))

    def test_test_normal_next_car_sequence_includes_get_in_and_excludes_perk_unlock(
        self,
    ) -> None:
        actions = build_auto3_normal_next_car_test_actions(self.profile_data)
        key_presses = _key_presses(actions)
        perk_path = _perk_path()

        self.assertEqual(key_presses[:3], ["down", "enter", "enter"])
        self.assertIn(_normal_next_car_menu_navigation(), _windows(key_presses, 10))
        self.assertNotIn(perk_path, _windows(key_presses, len(perk_path)))
        self.assertNotIn(1.5, _wait_durations(actions))

    def test_normal_next_car_test_uses_corrected_menu_navigation_after_get_in(
        self,
    ) -> None:
        actions = build_auto3_normal_next_car_test_actions(self.profile_data)
        key_presses = _key_presses(actions)

        self.assertEqual(key_presses[:3], ["down", "enter", "enter"])
        self.assertEqual(key_presses[3:], _normal_next_car_menu_navigation())

    def test_real_input_normal_next_car_test_starts_with_sort_setup_before_get_in(
        self,
    ) -> None:
        actions = build_auto3_real_input_normal_next_car_test_actions(
            self.profile_data
        )
        key_presses = _key_presses(actions)

        self.assertEqual(key_presses[:8], ["x"] + ["down"] * 6 + ["enter"])
        self.assertEqual(key_presses[8:11], ["down", "enter", "enter"])
        self.assertEqual(key_presses[11:], _normal_next_car_menu_navigation())
        self.assertNotIn(_perk_path(), _windows(key_presses, len(_perk_path())))

    def test_full_first_car_uses_escape_navigation_variant(self) -> None:
        actions = build_auto3_cycle_actions(self.profile_data, is_first_car=True)
        key_presses = _key_presses(actions)

        self.assertIn(_first_car_menu_navigation(), _windows(key_presses, 11))

    def test_full_normal_next_car_uses_no_escape_navigation_variant(self) -> None:
        actions = build_auto3_cycle_actions(self.profile_data, is_first_car=False)
        key_presses = _key_presses(actions)

        self.assertEqual(key_presses[:3], ["down", "enter", "enter"])
        self.assertEqual(key_presses[3:13], _normal_next_car_menu_navigation())

    def test_multi_car_test_count_one_uses_first_car_test_path_only(self) -> None:
        actions = build_auto3_multi_car_test_actions(1, self.profile_data)
        expected_actions = (
            build_auto3_first_car_exception_test_actions(self.profile_data)
            + build_auto3_test_mode_return_to_grid_actions(self.profile_data)
        )

        self.assertEqual(
            _key_presses(actions),
            _key_presses(expected_actions),
        )

    def test_multi_car_test_count_two_includes_reset_before_first_movement(
        self,
    ) -> None:
        actions = build_auto3_multi_car_test_actions(2, self.profile_data)
        key_presses = _key_presses(actions)
        first_car_keys = _key_presses(
            build_auto3_first_car_exception_test_actions(self.profile_data)
        )
        reset_keys = _key_presses(
            build_auto3_test_mode_return_to_grid_actions(self.profile_data)
        )
        expected_after_first_car = (
            reset_keys
            + ["down"]
            + _key_presses(build_auto3_get_in_hovered_car_actions(self.profile_data))
            + _normal_next_car_menu_navigation()
            + reset_keys
        )

        self.assertEqual(key_presses[: len(first_car_keys)], first_car_keys)
        self.assertEqual(key_presses[len(first_car_keys) :], expected_after_first_car)

    def test_multi_car_test_count_two_does_not_duplicate_a1_to_b1_down(
        self,
    ) -> None:
        actions = build_auto3_multi_car_test_actions(2, self.profile_data)
        key_presses = _key_presses(actions)
        reset_keys = _key_presses(
            build_auto3_test_mode_return_to_grid_actions(self.profile_data)
        )

        self.assertIn(
            reset_keys + ["down", "enter", "enter"],
            _windows(key_presses, len(reset_keys) + 3),
        )
        self.assertNotIn(
            reset_keys + ["down", "down", "enter", "enter"],
            _windows(key_presses, len(reset_keys) + 4),
        )

    def test_multi_car_test_count_three_does_not_duplicate_b1_to_c1_down(
        self,
    ) -> None:
        actions = build_auto3_multi_car_test_actions(3, self.profile_data)
        key_presses = _key_presses(actions)
        reset_keys = _key_presses(
            build_auto3_test_mode_return_to_grid_actions(self.profile_data)
        )

        self.assertIn(
            reset_keys + ["down", "enter", "enter"],
            _windows(key_presses, len(reset_keys) + 3),
        )
        self.assertNotIn(
            reset_keys + ["down", "down", "enter", "enter"],
            _windows(key_presses, len(reset_keys) + 4),
        )

    def test_multi_car_test_count_four_uses_column_transition_then_get_in(
        self,
    ) -> None:
        actions = build_auto3_multi_car_test_actions(4, self.profile_data)
        key_presses = _key_presses(actions)
        reset_keys = _key_presses(
            build_auto3_test_mode_return_to_grid_actions(self.profile_data)
        )

        self.assertIn(["right", "up", "up"], _windows(key_presses, 3))
        self.assertIn(
            reset_keys + ["right", "up", "up", "enter", "enter"],
            _windows(key_presses, len(reset_keys) + 5),
        )

    def test_multi_car_test_excludes_perk_unlock_path(self) -> None:
        actions = build_auto3_multi_car_test_actions(4, self.profile_data)
        key_presses = _key_presses(actions)

        self.assertNotIn(_perk_path(), _windows(key_presses, len(_perk_path())))
        self.assertNotIn(1.5, _wait_durations(actions))

    def test_multi_car_test_invalid_car_count_fails_clearly(self) -> None:
        with self.assertRaisesRegex(ValueError, "car_count must be greater than 0"):
            build_auto3_multi_car_test_actions(0, self.profile_data)

        with self.assertRaisesRegex(ValueError, "car_count must be an integer"):
            build_auto3_multi_car_test_actions("1", self.profile_data)

    def test_multi_car_unlock_count_one_includes_first_car_unlock_and_reset(
        self,
    ) -> None:
        actions = build_auto3_multi_car_unlock_actions(1, self.profile_data)
        expected_actions = build_auto3_first_car_exception_actions(self.profile_data)
        key_presses = _key_presses(actions)
        reset_keys = _key_presses(build_auto3_return_and_resort_actions(self.profile_data))

        self.assertEqual(key_presses, _key_presses(expected_actions))
        self.assertTrue(key_presses[-len(reset_keys) :] == reset_keys)
        self.assertNotIn(
            reset_keys + ["down", "enter", "enter"],
            _windows(key_presses, len(reset_keys) + 3),
        )
        self.assertEqual(1, _count_perk_paths(actions))

    def test_multi_car_unlock_count_two_uses_reset_movement_hover_get_in_and_unlock(
        self,
    ) -> None:
        actions = build_auto3_multi_car_unlock_actions(2, self.profile_data)
        key_presses = _key_presses(actions)
        reset_keys = _key_presses(
            build_auto3_return_and_resort_actions(self.profile_data)
        )
        expected_key_presses = (
            _key_presses(build_auto3_first_car_exception_actions(self.profile_data))
            + ["down"]
            + ["enter", "enter"]
            + _key_presses(
                build_auto3_post_get_in_car_mastery_navigation_actions(
                    self.profile_data
                )
            )
            + _perk_path()
            + ["esc", "esc"]
            + reset_keys
        )

        self.assertEqual(key_presses, expected_key_presses)
        self.assertIn(
            reset_keys + ["down", "enter", "enter", "esc"] + ["up"] * 6,
            _windows(key_presses, len(reset_keys) + 10),
        )
        self.assertTrue(key_presses[-len(reset_keys) :] == reset_keys)
        self.assertNotIn(
            reset_keys + ["down", "enter", "enter"],
            _windows(key_presses[-len(reset_keys) :], len(reset_keys) + 3),
        )
        self.assertNotIn(
            ["down", "enter", "enter"] + _normal_next_car_menu_navigation(),
            _windows(key_presses, 13),
        )
        self.assertEqual(2, _count_perk_paths(actions))

    def test_multi_car_unlock_count_two_waits_after_later_car_get_in(self) -> None:
        actions = build_auto3_multi_car_unlock_actions(2, self.profile_data)
        later_car_start = _find_key_path_start(
            actions,
            ["down", "enter", "enter", "esc"] + ["up"] * 6,
        )

        self.assertIsInstance(actions[later_car_start], KeyPressAction)
        self.assertEqual(actions[later_car_start].key, "down")
        self.assertIsInstance(actions[later_car_start + 1], WaitAction)
        self.assertIsInstance(actions[later_car_start + 2], KeyPressAction)
        self.assertEqual(actions[later_car_start + 2].key, "enter")
        self.assertIsInstance(actions[later_car_start + 3], WaitAction)
        self.assertEqual(actions[later_car_start + 3].duration_seconds, 1.0)
        self.assertIsInstance(actions[later_car_start + 4], KeyPressAction)
        self.assertEqual(actions[later_car_start + 4].key, "enter")
        self.assertIsInstance(actions[later_car_start + 5], WaitAction)
        self.assertEqual(actions[later_car_start + 5].duration_seconds, 12.0)

    def test_multi_car_unlock_count_four_includes_column_transition(self) -> None:
        actions = build_auto3_multi_car_unlock_actions(4, self.profile_data)
        key_presses = _key_presses(actions)

        self.assertIn(["right", "up", "up", "enter", "enter"], _windows(key_presses, 5))
        self.assertEqual(4, _count_perk_paths(actions))

    def test_multi_car_unlock_uses_skill_tree_delay_only_inside_unlock_path(
        self,
    ) -> None:
        actions = build_auto3_multi_car_unlock_actions(2, self.profile_data)
        perk_path = _perk_path()
        perk_starts = _find_all_key_path_starts(actions, perk_path)

        self.assertEqual(2, len(perk_starts))

        allowed_skill_tree_wait_indices = set()
        for perk_start in perk_starts:
            for action_index in range(perk_start + 1, perk_start + len(perk_path) * 2, 2):
                allowed_skill_tree_wait_indices.add(action_index)

        for action_index, action in enumerate(actions):
            if isinstance(action, WaitAction) and action.duration_seconds == 1.5:
                self.assertIn(action_index, allowed_skill_tree_wait_indices)

    def test_multi_car_unlock_invalid_car_count_fails_clearly(self) -> None:
        with self.assertRaisesRegex(ValueError, "car_count must be greater than 0"):
            build_auto3_multi_car_unlock_actions(0, self.profile_data)

        with self.assertRaisesRegex(ValueError, "car_count must be an integer"):
            build_auto3_multi_car_unlock_actions("1", self.profile_data)


class Auto3RunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.profile_data = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
        for timing_key in self.profile_data["timings"]:
            self.profile_data["timings"][timing_key] = 0.0

    def test_runner_completes_one_cycle_through_shared_systems(self) -> None:
        backend = InMemoryInputBackend()
        input_controller = InputController(backend)

        result = run_auto3_cycle(
            input_controller=input_controller,
            profile_data=self.profile_data,
        )

        self.assertTrue(result.completed)
        self.assertFalse(result.stopped)
        self.assertFalse(result.failed)
        self.assertEqual(input_controller.held_keys, frozenset())
        self.assertIn("enter", backend.pressed_keys)
        self.assertIn("esc", backend.pressed_keys)

    def test_runner_reports_stopped_outcome(self) -> None:
        stop_manager = StopManager()
        stop_manager.request_stop()
        input_controller = InputController(InMemoryInputBackend())

        result = run_auto3_cycle(
            input_controller=input_controller,
            stop_manager=stop_manager,
            profile_data=self.profile_data,
        )

        self.assertTrue(result.stopped)
        self.assertFalse(result.completed)
        self.assertFalse(result.failed)
        self.assertEqual(input_controller.held_keys, frozenset())

    def test_runner_reports_failed_outcome(self) -> None:
        input_controller = InputController(InMemoryInputBackend())

        result = run_auto3_cycle(
            input_controller=input_controller,
            profile_data=self.profile_data,
            action_builder=lambda profile_data: (_ for _ in ()).throw(
                ValueError("builder failed")
            ),
        )

        self.assertTrue(result.failed)
        self.assertFalse(result.completed)
        self.assertFalse(result.stopped)
        self.assertIn("builder failed", result.message)
        self.assertEqual(input_controller.held_keys, frozenset())


def _windows(values: list[str], window_size: int) -> list[list[str]]:
    return [
        values[index : index + window_size]
        for index in range(0, len(values) - window_size + 1)
    ]


def _wait_durations(actions) -> list[float]:
    return [
        action.duration_seconds
        for action in actions
        if isinstance(action, WaitAction)
    ]


def _find_key_path_start(actions, expected_keys: list[str]) -> int:
    for action_index in range(len(actions)):
        if not isinstance(actions[action_index], KeyPressAction):
            continue

        key_path = []
        candidate_index = action_index

        while candidate_index < len(actions) and len(key_path) < len(expected_keys):
            action = actions[candidate_index]
            if isinstance(action, KeyPressAction):
                key_path.append(action.key)
            candidate_index += 1

        if key_path == expected_keys:
            return action_index

    raise AssertionError(f"Expected key path was not found: {expected_keys}")


def _find_all_key_path_starts(actions, expected_keys: list[str]) -> list[int]:
    starts = []

    for action_index in range(len(actions)):
        if not isinstance(actions[action_index], KeyPressAction):
            continue

        key_path = []
        candidate_index = action_index

        while candidate_index < len(actions) and len(key_path) < len(expected_keys):
            action = actions[candidate_index]
            if isinstance(action, KeyPressAction):
                key_path.append(action.key)
            candidate_index += 1

        if key_path == expected_keys:
            starts.append(action_index)

    return starts


def _count_perk_paths(actions) -> int:
    return len(_find_all_key_path_starts(actions, _perk_path()))


def _perk_path() -> list[str]:
    return [
        "enter",
        "right",
        "enter",
        "up",
        "enter",
        "up",
        "enter",
        "up",
        "enter",
        "left",
        "enter",
    ]


def _first_car_menu_navigation() -> list[str]:
    return ["esc", "down", "enter"] + ["down"] * 7 + ["enter"]


def _normal_next_car_menu_navigation() -> list[str]:
    return ["down", "enter"] + ["down"] * 7 + ["enter"]


if __name__ == "__main__":
    unittest.main()
