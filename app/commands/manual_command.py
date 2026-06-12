from dataclasses import dataclass, field
from enum import Enum
from typing import Protocol

from app_logging.log_manager import ProjectLogger


APP_TITLE = "FH6 Farm Tool"


@dataclass(frozen=True)
class ConfirmationRequirement:
    flag_name: str
    is_confirmed: bool


class CommandStatus(str, Enum):
    COMPLETED = "completed"
    FAILED = "failed"
    REFUSED = "refused"
    STOPPED = "stopped"


class RiskLevel(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RefusalReason(str, Enum):
    MISSING_CONFIRMATION = "missing_confirmation"
    INVALID_COUNT = "invalid_count"
    INVALID_PROFILE = "invalid_profile"
    INVALID_VALUE = "invalid_value"
    UNSUPPORTED_OPERATION = "unsupported_operation"


@dataclass(frozen=True)
class OperatorMessage:
    message: str
    required_action: str | None = None
    suggested_next_step: str | None = None
    risk_level: RiskLevel = RiskLevel.INFO


@dataclass(frozen=True)
class CommandResult:
    status: CommandStatus
    command: str
    reason: str
    operator_message: OperatorMessage
    details: list[tuple[str, object]] = field(default_factory=list)
    refusal_reason: RefusalReason | None = None


@dataclass(frozen=True)
class PreflightResult:
    command: str
    passed: bool
    issues: list[CommandResult] = field(default_factory=list)


@dataclass(frozen=True)
class RunSummary:
    status: CommandStatus
    command: str
    fields: list[tuple[str, object]] = field(default_factory=list)
    operator_message: OperatorMessage | None = None


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

        result = CommandResult(
            status=CommandStatus.REFUSED,
            command=command_label,
            reason="Missing required confirmation flag.",
            refusal_reason=RefusalReason.MISSING_CONFIRMATION,
            operator_message=OperatorMessage(
                message=(
                    f"{command_label} requires --{confirmation.flag_name} "
                    "before it can continue."
                ),
                required_action=f"Re-run the command with --{confirmation.flag_name}.",
                suggested_next_step=(
                    "Only confirm when the FH6 baseline and command risk are understood."
                ),
                risk_level=RiskLevel.MEDIUM,
            ),
            details=[("Missing flag", f"--{confirmation.flag_name}")],
        )
        logger.warning(result.operator_message.message, category="sequence")
        print_refusal(result)
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
        result = _build_count_refusal(
            command_label=command_label,
            count_label="cycles",
            reason="Cycle count must be greater than 0.",
            required_action="Choose a cycle count greater than 0.",
        )
        logger.error(result.operator_message.message, category="error")
        print_refusal(result)
        return False

    if exact_count is not None and cycle_count != exact_count:
        result = _build_count_refusal(
            command_label=command_label,
            count_label="cycles",
            reason=f"Cycle count must be exactly {exact_count}.",
            required_action=f"Choose exactly {exact_count} cycle.",
            details=[("Required cycles", exact_count)],
        )
        logger.error(result.operator_message.message, category="error")
        print_refusal(result)
        return False

    if max_count is not None and cycle_count > max_count:
        result = _build_count_refusal(
            command_label=command_label,
            count_label="cycles",
            reason="Cycle count exceeds the current validated boundary.",
            required_action=f"Choose {max_count} or fewer cycles.",
            details=[("Current validated limit", f"{max_count} cycles")],
        )
        logger.error(result.operator_message.message, category="error")
        print_refusal(result)
        return False

    return True


def _build_count_refusal(
    command_label: str,
    count_label: str,
    reason: str,
    required_action: str,
    details: list[tuple[str, object]] | None = None,
) -> CommandResult:
    return CommandResult(
        status=CommandStatus.REFUSED,
        command=command_label,
        reason=reason,
        refusal_reason=RefusalReason.INVALID_COUNT,
        operator_message=OperatorMessage(
            message=f"{command_label} cannot continue: {reason}",
            required_action=required_action,
            suggested_next_step="Re-run the command after correcting the value.",
            risk_level=RiskLevel.LOW,
        ),
        details=[("Count field", count_label), *(details or [])],
    )


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
    summary = RunSummary(
        status=CommandStatus(result.status),
        command="Manual command",
        fields=[
            ("Requested cycles", result.requested_cycles),
            ("Completed cycles", result.completed_cycles),
            ("Final status", result.status),
            *(
                [("Estimated cost", estimated_total_cost)]
                if estimated_total_cost is not None
                else []
            ),
        ],
        operator_message=_summary_message_for_status(result.status),
    )
    print_run_summary(summary)


def _summary_message_for_status(status: str) -> OperatorMessage | None:
    if status == CommandStatus.STOPPED:
        return OperatorMessage(
            message="Operator control returned.",
            suggested_next_step="Verify FH6 focus, held inputs, and baseline before rerunning.",
            risk_level=RiskLevel.MEDIUM,
        )

    if status == CommandStatus.COMPLETED:
        return OperatorMessage(
            message="Command completed within the requested finite boundary.",
            risk_level=RiskLevel.INFO,
        )

    if status == CommandStatus.FAILED:
        return OperatorMessage(
            message="Command failed before normal completion.",
            suggested_next_step="Review the error above and restore the FH6 baseline before retrying.",
            risk_level=RiskLevel.MEDIUM,
        )

    return None


def print_run_summary(summary: RunSummary) -> None:
    print()
    print("## Run Summary")
    print()

    if summary.status == CommandStatus.STOPPED:
        print("STOPPED SAFELY")
        print()

    for label, value in summary.fields:
        print(f"{label}: {value}")

    if summary.operator_message is not None:
        print()
        print(f"Message: {summary.operator_message.message}")

        if summary.operator_message.suggested_next_step is not None:
            print(f"Suggested next step: {summary.operator_message.suggested_next_step}")


def print_refusal(result: CommandResult | str) -> None:
    if isinstance(result, str):
        print("REFUSED")
        print()
        print(f"Reason: {result}")
        print()
        print(f"Refused: {result}")
        return

    print("REFUSED")
    print()
    print(f"Command: {result.command}")
    print()
    print(f"Reason: {result.reason}")

    if result.details:
        print()
        for label, value in result.details:
            print(f"{label}: {value}")

    print()
    print(f"Message: {result.operator_message.message}")

    if result.operator_message.required_action is not None:
        print(f"Required action: {result.operator_message.required_action}")

    if result.operator_message.suggested_next_step is not None:
        print(f"Suggested next step: {result.operator_message.suggested_next_step}")

    print(f"Risk: {result.operator_message.risk_level.value}")
    print()
    print(f"Refused: {result.operator_message.message}")


def print_error(message: str) -> None:
    print(f"Error: {message}")


def print_info_summary(title: str, fields: list[tuple[str, object]]) -> None:
    print(title)
    print()

    for label, value in fields:
        print(f"{label}: {value}")
