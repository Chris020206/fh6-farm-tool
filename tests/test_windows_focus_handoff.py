import inspect
import unittest

from integrations import windows_focus_handoff
from integrations.windows_focus_handoff import (
    FocusHandoffStatus,
    WindowCandidate,
    attempt_fh6_focus_handoff,
    find_exact_title_matches,
    filter_fh6_window_candidates,
    select_focus_candidate,
    title_matches_fh6,
)


class WindowsFocusHandoffTest(unittest.TestCase):
    def test_title_matching_identifies_likely_fh6_titles(self) -> None:
        self.assertTrue(title_matches_fh6("Forza Horizon 6"))
        self.assertTrue(title_matches_fh6("FH6"))
        self.assertTrue(title_matches_fh6("Forza Horizon"))
        self.assertFalse(title_matches_fh6("Notepad"))

    def test_candidate_filtering_returns_likely_fh6_windows(self) -> None:
        candidates = filter_fh6_window_candidates(
            (
                WindowCandidate(handle=1, title="Notepad"),
                WindowCandidate(handle=2, title="Forza Horizon 6"),
                WindowCandidate(handle=3, title="FH6 - capture"),
            )
        )

        self.assertEqual(
            (
                WindowCandidate(handle=2, title="Forza Horizon 6"),
                WindowCandidate(handle=3, title="FH6 - capture"),
            ),
            candidates,
        )

    def test_select_candidate_requires_exact_title_for_multiple_candidates(self) -> None:
        candidates = (
            WindowCandidate(handle=2, title="Forza Horizon 6"),
            WindowCandidate(handle=3, title="FH6 - capture"),
        )

        self.assertIsNone(select_focus_candidate(candidates))
        self.assertEqual(
            WindowCandidate(handle=3, title="FH6 - capture"),
            select_focus_candidate(candidates, exact_title="FH6 - capture"),
        )

    def test_exact_target_title_match_finds_one_candidate(self) -> None:
        candidates = (
            WindowCandidate(handle=2, title="Forza Horizon 6"),
            WindowCandidate(
                handle=3,
                title="Forza Horizon 6 farm program - Repo Review and Findings - Google Chrome",
            ),
        )

        self.assertEqual(
            (WindowCandidate(handle=2, title="Forza Horizon 6"),),
            find_exact_title_matches(candidates, exact_title="Forza Horizon 6"),
        )

    def test_exact_target_title_selects_one_candidate_for_focus(self) -> None:
        result = attempt_fh6_focus_handoff(
            confirm_focus=True,
            exact_title="Forza Horizon 6",
            os_name="nt",
            window_provider=lambda: (
                WindowCandidate(handle=2, title="Forza Horizon 6"),
                WindowCandidate(
                    handle=3,
                    title="Forza Horizon 6 farm program - Repo Review and Findings - Google Chrome",
                ),
            ),
            focus_provider=lambda candidate: candidate.handle == 2,
        )

        self.assertEqual(FocusHandoffStatus.FOCUS_SUCCEEDED, result.status)
        self.assertEqual(
            WindowCandidate(handle=2, title="Forza Horizon 6"),
            result.selected_candidate,
        )

    def test_no_exact_target_match_refuses(self) -> None:
        result = attempt_fh6_focus_handoff(
            confirm_focus=True,
            exact_title="Forza Horizon 6",
            os_name="nt",
            window_provider=lambda: (
                WindowCandidate(
                    handle=3,
                    title="Forza Horizon 6 farm program - Repo Review and Findings - Google Chrome",
                ),
            ),
            focus_provider=lambda _candidate: True,
        )

        self.assertEqual(FocusHandoffStatus.REFUSED_TARGET_NOT_FOUND, result.status)
        self.assertFalse(result.focus_attempted)

    def test_duplicate_exact_target_match_refuses(self) -> None:
        result = attempt_fh6_focus_handoff(
            confirm_focus=True,
            exact_title="Forza Horizon 6",
            os_name="nt",
            window_provider=lambda: (
                WindowCandidate(handle=2, title="Forza Horizon 6"),
                WindowCandidate(handle=3, title="Forza Horizon 6"),
            ),
            focus_provider=lambda _candidate: True,
        )

        self.assertEqual(
            FocusHandoffStatus.REFUSED_DUPLICATE_TARGET_TITLE,
            result.status,
        )
        self.assertFalse(result.focus_attempted)

    def test_refuses_without_confirmation_and_does_not_focus(self) -> None:
        def fail_if_called(_candidate: WindowCandidate) -> bool:
            raise AssertionError("focus provider should not be called")

        result = attempt_fh6_focus_handoff(
            confirm_focus=False,
            os_name="nt",
            window_provider=lambda: (
                WindowCandidate(handle=2, title="Forza Horizon 6"),
            ),
            focus_provider=fail_if_called,
        )

        self.assertEqual(FocusHandoffStatus.REFUSED_MISSING_CONFIRMATION, result.status)
        self.assertFalse(result.focus_attempted)
        self.assertFalse(result.succeeded)

    def test_target_title_still_requires_confirmation(self) -> None:
        result = attempt_fh6_focus_handoff(
            confirm_focus=False,
            exact_title="Forza Horizon 6",
            os_name="nt",
            window_provider=lambda: (
                WindowCandidate(handle=2, title="Forza Horizon 6"),
                WindowCandidate(
                    handle=3,
                    title="Forza Horizon 6 farm program - Repo Review and Findings - Google Chrome",
                ),
            ),
            focus_provider=lambda _candidate: True,
        )

        self.assertEqual(FocusHandoffStatus.REFUSED_MISSING_CONFIRMATION, result.status)
        self.assertFalse(result.focus_attempted)

    def test_refuses_on_non_windows(self) -> None:
        result = attempt_fh6_focus_handoff(
            confirm_focus=True,
            os_name="posix",
            window_provider=lambda: (
                WindowCandidate(handle=2, title="Forza Horizon 6"),
            ),
        )

        self.assertEqual(FocusHandoffStatus.REFUSED_NON_WINDOWS, result.status)
        self.assertFalse(result.focus_attempted)

    def test_refuses_when_no_window_candidates_exist(self) -> None:
        result = attempt_fh6_focus_handoff(
            confirm_focus=True,
            os_name="nt",
            window_provider=lambda: (WindowCandidate(handle=1, title="Notepad"),),
        )

        self.assertEqual(FocusHandoffStatus.REFUSED_NO_CANDIDATES, result.status)
        self.assertFalse(result.focus_attempted)

    def test_refuses_multiple_candidates_without_exact_target(self) -> None:
        result = attempt_fh6_focus_handoff(
            confirm_focus=True,
            os_name="nt",
            window_provider=lambda: (
                WindowCandidate(handle=2, title="Forza Horizon 6"),
                WindowCandidate(handle=3, title="FH6 - capture"),
            ),
        )

        self.assertEqual(FocusHandoffStatus.REFUSED_MULTIPLE_CANDIDATES, result.status)
        self.assertFalse(result.focus_attempted)

    def test_reports_successful_focus_attempt(self) -> None:
        result = attempt_fh6_focus_handoff(
            confirm_focus=True,
            os_name="nt",
            window_provider=lambda: (
                WindowCandidate(handle=2, title="Forza Horizon 6"),
            ),
            focus_provider=lambda _candidate: True,
        )

        self.assertEqual(FocusHandoffStatus.FOCUS_SUCCEEDED, result.status)
        self.assertTrue(result.focus_attempted)
        self.assertTrue(result.succeeded)

    def test_focus_confirmation_retries_until_foreground_matches(self) -> None:
        foreground_states = iter(
            (
                WindowCandidate(handle=9, title="Other window"),
                WindowCandidate(handle=2, title="Forza Horizon 6"),
            )
        )
        observed_attempts: list[tuple[int, WindowCandidate | None]] = []

        result = attempt_fh6_focus_handoff(
            confirm_focus=True,
            exact_title="Forza Horizon 6",
            os_name="nt",
            window_provider=lambda: (
                WindowCandidate(handle=2, title="Forza Horizon 6"),
            ),
            focus_provider=lambda _candidate: False,
            foreground_provider=lambda: next(foreground_states),
            confirmation_observer=lambda attempt, active: observed_attempts.append(
                (attempt, active)
            ),
            confirmation_attempts=3,
            confirmation_delay_seconds=0,
        )

        self.assertEqual(FocusHandoffStatus.FOCUS_SUCCEEDED, result.status)
        self.assertEqual(
            WindowCandidate(handle=2, title="Forza Horizon 6"),
            result.active_candidate,
        )
        self.assertEqual(
            [
                (1, WindowCandidate(handle=9, title="Other window")),
                (2, WindowCandidate(handle=2, title="Forza Horizon 6")),
            ],
            observed_attempts,
        )

    def test_focus_failure_reports_active_window_and_attempt_count(self) -> None:
        result = attempt_fh6_focus_handoff(
            confirm_focus=True,
            exact_title="Forza Horizon 6",
            os_name="nt",
            window_provider=lambda: (
                WindowCandidate(handle=2, title="Forza Horizon 6"),
            ),
            focus_provider=lambda _candidate: False,
            foreground_provider=lambda: WindowCandidate(handle=9, title="Browser"),
            confirmation_attempts=2,
            confirmation_delay_seconds=0,
        )

        self.assertEqual(FocusHandoffStatus.FOCUS_FAILED, result.status)
        self.assertEqual(WindowCandidate(handle=9, title="Browser"), result.active_candidate)
        self.assertEqual(2, result.confirmation_attempts)
        self.assertTrue(result.focus_attempted)
        self.assertFalse(result.succeeded)

    def test_focus_handoff_module_does_not_import_automation_execution(self) -> None:
        source = inspect.getsource(windows_focus_handoff)

        self.assertNotIn("automation.", source)
        self.assertNotIn("core.input", source)
        self.assertNotIn("SequenceRunner", source)


if __name__ == "__main__":
    unittest.main()
