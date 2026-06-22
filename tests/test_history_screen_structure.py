import unittest
from datetime import datetime, timezone

from sessions.operational_history import OperationalHistoryEntry
from sessions.session_status import SessionStatus
from ui.history_screen import (
    HistoryFilterState,
    HistorySectionId,
    build_history_screen,
)


class HistoryScreenStructureTest(unittest.TestCase):
    def test_most_recent_sessions_appear_first(self) -> None:
        older_entry = _history_entry(
            session_id="older-session",
            timestamp=datetime(2026, 6, 13, 10, 0, 0, tzinfo=timezone.utc),
        )
        recent_entry = _history_entry(
            session_id="recent-session",
            timestamp=datetime(2026, 6, 13, 11, 0, 0, tzinfo=timezone.utc),
        )

        screen = build_history_screen((older_entry, recent_entry))

        self.assertEqual(
            "recent-session",
            screen.recent_sessions.sessions[0].session_id,
        )
        self.assertEqual(HistorySectionId.RECENT, screen.recent_sessions.section_id)

    def test_session_oriented_entries_are_used(self) -> None:
        entry = _history_entry(
            session_id="session-oriented",
            summary="Auto1 completed 2 of 2 requested run(s).",
        )

        screen = build_history_screen((entry,))
        summary = screen.recent_sessions.sessions[0]

        self.assertEqual("session-oriented", summary.session_id)
        self.assertEqual("Auto1", summary.automation_name)
        self.assertIn("completed 2 of 2", summary.summary)
        self.assertEqual(2, summary.requested_count)
        self.assertEqual(2, summary.completed_count)

    def test_raw_technical_references_are_not_exposed(self) -> None:
        entry = _history_entry(
            session_id="safe-session",
            summary="Auto2 did not start because confirmation was missing.",
            expandable_details=("Operator-facing detail only.",),
        )

        screen = build_history_screen((entry,))
        summary = screen.recent_sessions.sessions[0]
        serialized_values = " ".join(str(value) for value in summary.__dict__.values())

        self.assertNotIn("technical_reference", serialized_values)
        self.assertNotIn("keypress", serialized_values.lower())
        self.assertNotIn("debug", serialized_values.lower())
        self.assertNotIn("raw log", serialized_values.lower())

    def test_expandable_details_remain_optional_and_layered(self) -> None:
        entry_with_details = _history_entry(
            session_id="with-details",
            expandable_details=("Duration: 30.0 seconds.",),
        )
        entry_without_details = _history_entry(
            session_id="without-details",
            timestamp=datetime(2026, 6, 13, 9, 0, 0, tzinfo=timezone.utc),
            expandable_details=(),
        )

        screen = build_history_screen((entry_with_details, entry_without_details))
        with_details = screen.recent_sessions.sessions[0]
        without_details = screen.recent_sessions.sessions[1]

        self.assertTrue(with_details.detail_layer.is_available)
        self.assertFalse(with_details.detail_layer.is_expanded_by_default)
        self.assertFalse(without_details.detail_layer.is_available)

    def test_filters_are_secondary_not_primary(self) -> None:
        filters = HistoryFilterState(selected_statuses=(SessionStatus.STOPPED,))
        completed_entry = _history_entry(
            session_id="completed-session",
            outcome=SessionStatus.COMPLETED,
        )
        stopped_entry = _history_entry(
            session_id="stopped-session",
            outcome=SessionStatus.STOPPED,
        )

        screen = build_history_screen(
            (completed_entry, stopped_entry),
            filters=filters,
        )

        self.assertTrue(screen.filters.is_secondary)
        self.assertEqual(
            ("stopped-session",),
            tuple(session.session_id for session in screen.recent_sessions.sessions),
        )

    def test_screen_has_one_primary_intention(self) -> None:
        screen = build_history_screen(())

        self.assertEqual(
            "Recent FAA operation will appear here when recorded.",
            screen.primary_intention,
        )

    def test_empty_history_is_honest_and_contains_no_sessions(self) -> None:
        screen = build_history_screen(())

        self.assertFalse(screen.has_sessions)
        self.assertEqual((), screen.recent_sessions.sessions)
        self.assertIsNone(screen.older_sessions)
        self.assertIsNotNone(screen.empty_state)
        self.assertEqual(
            "No operational sessions recorded yet",
            screen.empty_state.title,
        )
        self.assertIn("once session history is connected", screen.empty_state.summary)
        self.assertIn("supervised live state", " ".join(screen.empty_state.details))

    def test_older_section_is_absent_until_recent_limit_is_exceeded(self) -> None:
        entries = tuple(
            _history_entry(
                session_id=f"session-{index}",
                timestamp=datetime(2026, 6, 13, 10, index, 0, tzinfo=timezone.utc),
            )
            for index in range(3)
        )

        screen = build_history_screen(entries, recent_limit=3)

        self.assertTrue(screen.has_sessions)
        self.assertIsNone(screen.empty_state)
        self.assertIsNone(screen.older_sessions)

    def test_session_summary_preserves_recovery_context_and_layered_details(self) -> None:
        entry = _history_entry(
            session_id="rich-session",
            requested_count=4,
            completed_count=2,
            warnings=("FH6 focus changed during operation.",),
            recovery_note="Return FH6 to the validated baseline.",
            suggested_next_step="Review readiness before retrying.",
            expandable_details=("Duration: 42.0 seconds.",),
        )

        summary = build_history_screen((entry,)).recent_sessions.sessions[0]

        self.assertEqual((4, 2), (summary.requested_count, summary.completed_count))
        self.assertEqual(entry.warnings, summary.warnings)
        self.assertEqual(entry.recovery_note, summary.recovery_note)
        self.assertEqual(entry.suggested_next_step, summary.suggested_next_step)
        self.assertTrue(summary.detail_layer.is_available)
        self.assertEqual(entry.expandable_details, summary.detail_layer.details)

    def test_completed_stopped_interrupted_refused_prepared_states_are_calm(self) -> None:
        statuses = (
            SessionStatus.COMPLETED,
            SessionStatus.STOPPED,
            SessionStatus.INTERRUPTED,
            SessionStatus.REFUSED,
            SessionStatus.PREPARED,
        )
        entries = tuple(
            _history_entry(
                session_id=f"{status.value}-session",
                outcome=status,
                timestamp=datetime(2026, 6, 13, 10, index, 0, tzinfo=timezone.utc),
            )
            for index, status in enumerate(statuses)
        )

        screen = build_history_screen(entries, recent_limit=len(entries))
        outcome_messages = tuple(
            session.outcome_message
            for session in screen.recent_sessions.sessions
        )

        self.assertEqual(len(statuses), len(outcome_messages))
        for outcome_message in outcome_messages:
            self.assertNotIn("panic", outcome_message.lower())
            self.assertNotIn("guaranteed", outcome_message.lower())
            self.assertTrue(outcome_message.strip())

    def test_older_sessions_are_secondary(self) -> None:
        entries = tuple(
            _history_entry(
                session_id=f"session-{index}",
                timestamp=datetime(2026, 6, 13, 10, index, 0, tzinfo=timezone.utc),
            )
            for index in range(5)
        )

        screen = build_history_screen(entries, recent_limit=3)

        self.assertEqual(3, len(screen.recent_sessions.sessions))
        self.assertIsNotNone(screen.older_sessions)
        self.assertEqual(2, len(screen.older_sessions.sessions))
        self.assertEqual(HistorySectionId.OLDER, screen.older_sessions.section_id)
        self.assertIn("Secondary", screen.older_sessions.purpose)


def _history_entry(
    session_id: str,
    timestamp: datetime | None = None,
    outcome: SessionStatus = SessionStatus.COMPLETED,
    summary: str = "Auto1 completed 2 of 2 requested run(s).",
    expandable_details: tuple[str, ...] = (),
    requested_count: int = 2,
    completed_count: int | None = None,
    warnings: tuple[str, ...] = (),
    recovery_note: str | None = None,
    suggested_next_step: str | None = "Review baseline before another run.",
) -> OperationalHistoryEntry:
    return OperationalHistoryEntry(
        session_id=session_id,
        automation_id="auto1",
        automation_name="Auto1",
        profile_id="auto1_race_default",
        profile_name="Auto1 Race Default",
        outcome=outcome,
        summary=summary,
        timestamp=timestamp
        or datetime(2026, 6, 13, 10, 0, 0, tzinfo=timezone.utc),
        requested_count=requested_count,
        completed_count=(
            completed_count
            if completed_count is not None
            else (requested_count if outcome == SessionStatus.COMPLETED else 1)
        ),
        confidence_note="Session summary is available for operator review.",
        warnings=warnings,
        recovery_note=recovery_note,
        suggested_next_step=suggested_next_step,
        expandable_details=expandable_details,
    )


if __name__ == "__main__":
    unittest.main()
