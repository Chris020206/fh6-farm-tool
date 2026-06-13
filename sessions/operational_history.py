from dataclasses import dataclass, field
from datetime import datetime

from product.automation_registry import get_automation_definition
from product.profile_metadata_registry import get_profile_metadata
from sessions.run_session import RunSession
from sessions.session_status import SessionStatus


@dataclass(frozen=True)
class OperationalHistoryEntry:
    session_id: str
    automation_id: str
    automation_name: str
    profile_id: str
    profile_name: str
    outcome: SessionStatus
    summary: str
    timestamp: datetime
    requested_count: int
    completed_count: int
    confidence_note: str
    warnings: tuple[str, ...] = field(default_factory=tuple)
    recovery_note: str | None = None
    suggested_next_step: str | None = None
    expandable_details: tuple[str, ...] = field(default_factory=tuple)


def derive_operational_history_entry(
    run_session: RunSession,
) -> OperationalHistoryEntry:
    automation_definition = get_automation_definition(run_session.automation_id)
    profile_metadata = get_profile_metadata(run_session.profile_id)
    timestamp = run_session.ended_at or run_session.started_at

    return OperationalHistoryEntry(
        session_id=run_session.session_id,
        automation_id=run_session.automation_id,
        automation_name=automation_definition.display_name,
        profile_id=run_session.profile_id,
        profile_name=profile_metadata.profile_name,
        outcome=run_session.status,
        summary=_build_summary(run_session, automation_definition.display_name),
        timestamp=timestamp,
        requested_count=run_session.requested_count,
        completed_count=run_session.completed_count,
        confidence_note=_build_confidence_note(run_session.status),
        warnings=run_session.warnings_encountered,
        recovery_note=_build_recovery_note(run_session),
        suggested_next_step=run_session.suggested_next_step
        or automation_definition.suggested_next_step,
        expandable_details=_build_expandable_details(run_session),
    )


def _build_summary(run_session: RunSession, automation_name: str) -> str:
    if run_session.user_facing_summary:
        return run_session.user_facing_summary

    if run_session.status == SessionStatus.COMPLETED:
        return (
            f"{automation_name} completed {run_session.completed_count} of "
            f"{run_session.requested_count} requested run(s)."
        )

    if run_session.status == SessionStatus.STOPPED:
        return (
            f"{automation_name} stopped after {run_session.completed_count} of "
            f"{run_session.requested_count} requested run(s)."
        )

    if run_session.status == SessionStatus.REFUSED:
        return f"{automation_name} did not start because a safety requirement was not met."

    if run_session.status == SessionStatus.INTERRUPTED:
        return f"{automation_name} was interrupted before the requested run was complete."

    if run_session.status == SessionStatus.FAILURE:
        return f"{automation_name} failed before completing the requested run."

    return f"{automation_name} is running."


def _build_confidence_note(status: SessionStatus) -> str:
    if status == SessionStatus.COMPLETED:
        return "Execution ended as expected for the recorded session."

    if status == SessionStatus.STOPPED:
        return "The operator stopped execution and the session returned to a controlled state."

    if status == SessionStatus.REFUSED:
        return "The session was refused before execution to preserve safety boundaries."

    if status == SessionStatus.INTERRUPTED:
        return "The session needs operator review before another run."

    if status == SessionStatus.FAILURE:
        return "The session failed and should be reviewed before retrying."

    return "Execution is still in progress."


def _build_recovery_note(run_session: RunSession) -> str | None:
    if run_session.stop_or_interruption_reason:
        return run_session.stop_or_interruption_reason

    if run_session.status in {
        SessionStatus.INTERRUPTED,
        SessionStatus.FAILURE,
        SessionStatus.STOPPED,
    }:
        return "Review FH6 baseline state before starting another run."

    return None


def _build_expandable_details(run_session: RunSession) -> tuple[str, ...]:
    details: list[str] = list(run_session.user_facing_notes)

    if run_session.duration_seconds is not None:
        details.append(f"Duration: {run_session.duration_seconds:.1f} seconds.")

    return tuple(details)
