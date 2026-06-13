import unittest
from datetime import datetime, timezone

from sessions.operational_history import derive_operational_history_entry
from sessions.run_session import RunSession
from sessions.session_status import SessionStatus


class RunSessionLayerTest(unittest.TestCase):
    def test_run_session_tracks_core_session_data(self) -> None:
        started_at = datetime(2026, 6, 13, 10, 0, 0, tzinfo=timezone.utc)
        ended_at = datetime(2026, 6, 13, 10, 0, 30, tzinfo=timezone.utc)

        run_session = RunSession(
            session_id="session-001",
            automation_id="auto1",
            profile_id="auto1_race_default",
            requested_count=2,
            completed_count=2,
            status=SessionStatus.COMPLETED,
            started_at=started_at,
            ended_at=ended_at,
            user_facing_summary="Auto1 completed the requested race cycles.",
        )

        self.assertEqual("session-001", run_session.session_id)
        self.assertEqual(SessionStatus.COMPLETED, run_session.status)
        self.assertEqual(30.0, run_session.duration_seconds)

    def test_operational_history_entry_is_derived_from_session(self) -> None:
        started_at = datetime(2026, 6, 13, 10, 0, 0, tzinfo=timezone.utc)
        ended_at = datetime(2026, 6, 13, 10, 1, 0, tzinfo=timezone.utc)
        run_session = RunSession(
            session_id="session-002",
            automation_id="auto3",
            profile_id="auto3_skill_tree_default",
            requested_count=4,
            completed_count=4,
            status=SessionStatus.COMPLETED,
            started_at=started_at,
            ended_at=ended_at,
            warnings_encountered=("Start row A assumption was used.",),
            user_facing_notes=("Validated traversal remained within the guarded boundary.",),
        )

        history_entry = derive_operational_history_entry(run_session)

        self.assertEqual("session-002", history_entry.session_id)
        self.assertIn("Auto3", history_entry.automation_name)
        self.assertIn("Skill Tree Automation", history_entry.automation_name)
        self.assertEqual("Auto3 Skill Tree Default", history_entry.profile_name)
        self.assertEqual(SessionStatus.COMPLETED, history_entry.outcome)
        self.assertIn("completed 4 of 4", history_entry.summary)
        self.assertEqual(("Start row A assumption was used.",), history_entry.warnings)
        self.assertIn(
            "Validated traversal remained within the guarded boundary.",
            history_entry.expandable_details,
        )

    def test_history_summary_uses_user_facing_summary_when_present(self) -> None:
        started_at = datetime(2026, 6, 13, 10, 0, 0, tzinfo=timezone.utc)
        run_session = RunSession(
            session_id="session-003",
            automation_id="auto2",
            profile_id="auto2_buy_car_default",
            requested_count=1,
            completed_count=0,
            status=SessionStatus.REFUSED,
            started_at=started_at,
            user_facing_summary="Auto2 did not start because purchase confirmation was missing.",
            technical_reference="internal-check:confirm-purchase",
        )

        history_entry = derive_operational_history_entry(run_session)

        self.assertEqual(
            "Auto2 did not start because purchase confirmation was missing.",
            history_entry.summary,
        )
        self.assertNotIn("internal-check", history_entry.summary)
        self.assertNotIn("internal-check", " ".join(history_entry.expandable_details))

    def test_stopped_session_gets_recovery_note(self) -> None:
        started_at = datetime(2026, 6, 13, 10, 0, 0, tzinfo=timezone.utc)
        run_session = RunSession(
            session_id="session-004",
            automation_id="auto1",
            profile_id="auto1_race_default",
            requested_count=25,
            completed_count=10,
            status=SessionStatus.STOPPED,
            started_at=started_at,
            stop_or_interruption_reason="Operator pressed F8 during execution.",
        )

        history_entry = derive_operational_history_entry(run_session)

        self.assertIn("stopped after 10 of 25", history_entry.summary)
        self.assertEqual(
            "Operator pressed F8 during execution.",
            history_entry.recovery_note,
        )

    def test_running_session_has_no_duration_until_ended(self) -> None:
        started_at = datetime(2026, 6, 13, 10, 0, 0, tzinfo=timezone.utc)
        run_session = RunSession(
            session_id="session-005",
            automation_id="auto1",
            profile_id="auto1_race_default",
            requested_count=1,
            completed_count=0,
            status=SessionStatus.RUNNING,
            started_at=started_at,
        )

        self.assertIsNone(run_session.duration_seconds)


if __name__ == "__main__":
    unittest.main()
