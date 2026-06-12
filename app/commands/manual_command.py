from dataclasses import dataclass
from typing import Protocol

from app_logging.log_manager import ProjectLogger


APP_TITLE = "FH6 Farm Tool"


@dataclass(frozen=True)
class ConfirmationRequirement:
    flag_name: str
    is_confirmed: bool


class ManualRunResult(Protocol):
    requested_cycles: int
    completed_cycles: int
    status: str


def require_confirmations(
    command_label: str,
    confirmations: list[ConfirmationRequirement],
    logger: ProjectLogger,
) -> bool:
    for confirmation in confirmations:
        if confirmation.is_confirmed:
            continue

        message = f"Missing required confirmation flag: --{confirmation.flag_name}."
        logger.warning(message, category="sequence")
        print_refusal(message)
        return False

    return True


def validate_cycle_count(
    cycle_count: int,
    command_label: str,
    logger: ProjectLogger,
    exact_count: int | None = None,
    max_count: int | None = None,
) -> bool:
    if cycle_count <= 0:
        message = f"{command_label} requires a cycle count greater than 0."
        logger.error(message, category="error")
        print_refusal(message)
        return False

    if exact_count is not None and cycle_count != exact_count:
        message = f"{command_label} requires cycles to be exactly {exact_count}."
        logger.error(message, category="error")
        print_refusal(message)
        return False

    if max_count is not None and cycle_count > max_count:
        message = (
            f"{command_label} requires cycles to be {max_count} or fewer."
        )
        logger.error(message, category="error")
        print_refusal(message)
        return False

    return True


def print_command_title(command_name: str) -> None:
    print(f"{APP_TITLE} - {command_name}")
    print()


def print_command_intro(
    command_name: str,
    warning_lines: list[str],
    requested_cycles: int | None = None,
    mode: str | None = None,
    profile: str | None = None,
    estimated_total_cost: float | int | None = None,
    notes: list[str] | None = None,
    f8_stop_available: bool = False,
) -> None:
    print_command_title(command_name)

    if mode is not None:
        print(f"Mode: {mode}")

    if profile is not None:
        print(f"Profile: {profile}")

    if requested_cycles is not None:
        print(f"Requested cycles: {requested_cycles}")

    if estimated_total_cost is not None:
        print(f"Estimated cost: {estimated_total_cost}")

    for note in notes or []:
        print(note)

    if warning_lines:
        print()
        for warning_line in warning_lines:
            print(f"WARNING: {warning_line}")

    if f8_stop_available:
        print()
        print("Press F8 to stop safely.")


def print_result_summary(
    result: ManualRunResult,
    estimated_total_cost: float | int | None = None,
) -> None:
    print()
    print("## Run Summary")
    print()
    print(f"Requested cycles: {result.requested_cycles}")
    print(f"Completed cycles: {result.completed_cycles}")
    print(f"Final status: {result.status}")

    if estimated_total_cost is not None:
        print(f"Estimated cost: {estimated_total_cost}")


def print_refusal(message: str) -> None:
    print(f"Refused: {message}")


def print_error(message: str) -> None:
    print(f"Error: {message}")


def print_info_summary(title: str, fields: list[tuple[str, object]]) -> None:
    print(title)
    print()

    for label, value in fields:
        print(f"{label}: {value}")
