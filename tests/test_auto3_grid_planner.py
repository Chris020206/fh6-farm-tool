import unittest
import json
from pathlib import Path

from automation.auto3_skill_tree.auto3_grid_planner import (
    GridPosition,
    build_auto3_grid_movement_actions,
    index_to_position,
    movement_between_indices,
    movement_from_index_to_next,
)
from core.actions import KeyPressAction, WaitAction


PROFILE_PATH = Path("profiles/official/auto3_skill_tree_default.json")


class Auto3GridPlannerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.profile_data = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))

    def test_index_zero_maps_to_a1(self) -> None:
        self.assertEqual(GridPosition(row=0, column=0), index_to_position(0))

    def test_index_one_maps_to_b1(self) -> None:
        self.assertEqual(GridPosition(row=1, column=0), index_to_position(1))

    def test_index_two_maps_to_c1(self) -> None:
        self.assertEqual(GridPosition(row=2, column=0), index_to_position(2))

    def test_index_three_maps_to_a2(self) -> None:
        self.assertEqual(GridPosition(row=0, column=1), index_to_position(3))

    def test_index_zero_to_one_returns_down(self) -> None:
        self.assertEqual(["down"], movement_from_index_to_next(0))

    def test_index_one_to_two_returns_down(self) -> None:
        self.assertEqual(["down"], movement_from_index_to_next(1))

    def test_index_two_to_three_returns_column_transition(self) -> None:
        self.assertEqual(["right", "up", "up"], movement_from_index_to_next(2))

    def test_movement_between_indices_rejects_non_next_target(self) -> None:
        with self.assertRaisesRegex(ValueError, "next-index movement only"):
            movement_between_indices(0, 2)

    def test_negative_index_fails_clearly(self) -> None:
        with self.assertRaisesRegex(ValueError, "greater than or equal to 0"):
            index_to_position(-1)

    def test_non_integer_index_fails_clearly(self) -> None:
        with self.assertRaisesRegex(ValueError, "must be an integer"):
            index_to_position("0")

    def test_down_movement_token_builds_key_press_and_delay(self) -> None:
        actions = build_auto3_grid_movement_actions(["down"], self.profile_data)

        self.assertEqual(["down"], _key_presses(actions))
        self.assertEqual([1.0], _wait_durations(actions))

    def test_column_transition_tokens_build_key_presses_and_delays(self) -> None:
        actions = build_auto3_grid_movement_actions(
            ["right", "up", "up"],
            self.profile_data,
        )

        self.assertEqual(["right", "up", "up"], _key_presses(actions))
        self.assertEqual([1.0, 1.0, 1.0], _wait_durations(actions))

    def test_unknown_movement_token_fails_clearly(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unknown Auto3 grid movement token"):
            build_auto3_grid_movement_actions(["left"], self.profile_data)


def _key_presses(actions) -> list[str]:
    return [
        action.key
        for action in actions
        if isinstance(action, KeyPressAction)
    ]


def _wait_durations(actions) -> list[float]:
    return [
        action.duration_seconds
        for action in actions
        if isinstance(action, WaitAction)
    ]


if __name__ == "__main__":
    unittest.main()
