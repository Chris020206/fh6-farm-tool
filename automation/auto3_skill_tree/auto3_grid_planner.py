from dataclasses import dataclass
from typing import Any

from automation.auto3_skill_tree.auto3_sequence import _load_auto3_profile_sections
from core.actions import BaseAction, KeyPressAction, WaitAction


@dataclass(frozen=True)
class GridPosition:
    row: int
    column: int


def index_to_position(index: int) -> GridPosition:
    _validate_index(index, "index")

    return GridPosition(
        row=index % 3,
        column=index // 3,
    )


def movement_from_index_to_next(index: int) -> list[str]:
    _validate_index(index, "index")

    return movement_between_indices(index, index + 1)


def movement_between_indices(from_index: int, to_index: int) -> list[str]:
    _validate_index(from_index, "from_index")
    _validate_index(to_index, "to_index")

    if to_index != from_index + 1:
        raise ValueError(
            "Auto3 grid movement currently supports next-index movement only."
        )

    from_position = index_to_position(from_index)
    to_position = index_to_position(to_index)

    if from_position.column == to_position.column:
        return _movement_within_column(from_position, to_position)

    if from_position.row == 2 and to_position.row == 0:
        return ["right", "up", "up"]

    raise ValueError(
        "Auto3 grid movement does not support the requested position change."
    )


def build_auto3_grid_movement_actions(
    movement_tokens: list[str],
    profile_data: dict[str, Any],
) -> list[BaseAction]:
    keys, _, timings = _load_auto3_profile_sections(profile_data)
    token_to_key = {
        "down": keys["down_key"],
        "up": keys["up_key"],
        "right": keys["right_key"],
    }

    actions: list[BaseAction] = []
    for movement_token in movement_tokens:
        if movement_token not in token_to_key:
            raise ValueError(f"Unknown Auto3 grid movement token: {movement_token}")

        actions.extend(
            [
                KeyPressAction(token_to_key[movement_token]),
                WaitAction(timings["menu_key_delay"]),
            ]
        )

    return actions


def _movement_within_column(
    from_position: GridPosition,
    to_position: GridPosition,
) -> list[str]:
    if to_position.row == from_position.row + 1:
        return ["down"]

    raise ValueError(
        "Auto3 grid movement within a column only supports moving down one row."
    )


def _validate_index(index: int, field_name: str) -> None:
    if not isinstance(index, int):
        raise ValueError(f"{field_name} must be an integer.")

    if index < 0:
        raise ValueError(f"{field_name} must be greater than or equal to 0.")
