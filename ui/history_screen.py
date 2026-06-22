from dataclasses import dataclass, field
from enum import Enum

from sessions.operational_history import OperationalHistoryEntry
from sessions.session_status import SessionStatus


class HistorySectionId(str, Enum):
    RECENT = "recent"
    OLDER = "older"


@dataclass(frozen=True)
class HistoryFilterState:
    selected_statuses: tuple[SessionStatus, ...] = field(default_factory=tuple)
    selected_automation_names: tuple[str, ...] = field(default_factory=tuple)
    is_secondary: bool = True


@dataclass(frozen=True)
class HistoryDetailLayer:
    details: tuple[str, ...]
    is_available: bool
    is_expanded_by_default: bool = False


@dataclass(frozen=True)
class HistorySessionSummary:
    session_id: str
    automation_name: str
    profile_name: str
    outcome: SessionStatus
    outcome_message: str
    summary: str
    timestamp_label: str
    requested_count: int
    completed_count: int
    confidence_note: str
    warnings: tuple[str, ...]
    recovery_note: str | None
    suggested_next_step: str | None
    detail_layer: HistoryDetailLayer


@dataclass(frozen=True)
class RecentSessionsSection:
    section_id: HistorySectionId
    purpose: str
    sessions: tuple[HistorySessionSummary, ...]


@dataclass(frozen=True)
class OlderSessionsSection:
    section_id: HistorySectionId
    purpose: str
    sessions: tuple[HistorySessionSummary, ...]


@dataclass(frozen=True)
class HistoryEmptyState:
    title: str
    summary: str
    details: tuple[str, ...]


@dataclass(frozen=True)
class HistoryScreen:
    primary_intention: str
    recent_sessions: RecentSessionsSection
    older_sessions: OlderSessionsSection | None
    filters: HistoryFilterState
    has_sessions: bool
    empty_state: HistoryEmptyState | None


def build_history_screen(
    history_entries: tuple[OperationalHistoryEntry, ...],
    filters: HistoryFilterState | None = None,
    recent_limit: int = 3,
) -> HistoryScreen:
    active_filters = filters or HistoryFilterState()
    sorted_entries = tuple(
        sorted(
            _apply_filters(history_entries, active_filters),
            key=lambda entry: entry.timestamp,
            reverse=True,
        )
    )
    recent_entries = sorted_entries[:recent_limit]
    older_entries = sorted_entries[recent_limit:]

    has_sessions = bool(sorted_entries)
    empty_state = None
    if not has_sessions:
        empty_state = HistoryEmptyState(
            title="No operational sessions recorded yet",
            summary=(
                "Completed, stopped, refused, interrupted, or failed sessions will "
                "appear here once session history is connected."
            ),
            details=(
                "Current desktop operation is still supervised live state, not stored history.",
                "Use the completion screen immediately after a run for the current result.",
            ),
        )

    return HistoryScreen(
        primary_intention="Recent FAA operation will appear here when recorded.",
        recent_sessions=RecentSessionsSection(
            section_id=HistorySectionId.RECENT,
            purpose="Most recent session-oriented operational memory.",
            sessions=tuple(_build_session_summary(entry) for entry in recent_entries),
        ),
        older_sessions=(
            OlderSessionsSection(
                section_id=HistorySectionId.OLDER,
                purpose="Secondary session history for earlier operational context.",
                sessions=tuple(_build_session_summary(entry) for entry in older_entries),
            )
            if older_entries
            else None
        ),
        filters=active_filters,
        has_sessions=has_sessions,
        empty_state=empty_state,
    )


def _apply_filters(
    history_entries: tuple[OperationalHistoryEntry, ...],
    filters: HistoryFilterState,
) -> tuple[OperationalHistoryEntry, ...]:
    filtered_entries = history_entries

    if filters.selected_statuses:
        filtered_entries = tuple(
            entry
            for entry in filtered_entries
            if entry.outcome in filters.selected_statuses
        )

    if filters.selected_automation_names:
        filtered_entries = tuple(
            entry
            for entry in filtered_entries
            if entry.automation_name in filters.selected_automation_names
        )

    return filtered_entries


def _build_session_summary(
    history_entry: OperationalHistoryEntry,
) -> HistorySessionSummary:
    details = tuple(history_entry.expandable_details)

    return HistorySessionSummary(
        session_id=history_entry.session_id,
        automation_name=history_entry.automation_name,
        profile_name=history_entry.profile_name,
        outcome=history_entry.outcome,
        outcome_message=_build_outcome_message(history_entry.outcome),
        summary=history_entry.summary,
        timestamp_label=history_entry.timestamp.isoformat(),
        requested_count=history_entry.requested_count,
        completed_count=history_entry.completed_count,
        confidence_note=history_entry.confidence_note,
        warnings=history_entry.warnings,
        recovery_note=history_entry.recovery_note,
        suggested_next_step=history_entry.suggested_next_step,
        detail_layer=HistoryDetailLayer(
            details=details,
            is_available=bool(details),
        ),
    )


def _build_outcome_message(status: SessionStatus) -> str:
    if status == SessionStatus.COMPLETED:
        return "Completed as expected."

    if status == SessionStatus.STOPPED:
        return "Stopped by the operator."

    if status == SessionStatus.INTERRUPTED:
        return "Interrupted before completion; review before retrying."

    if status == SessionStatus.REFUSED:
        return "Refused before execution to preserve safety."

    if status == SessionStatus.PREPARED:
        return "Prepared for review; execution has not started."

    if status == SessionStatus.RUNNING:
        return "Running session in progress."

    return "Ended with a failure; review before retrying."
