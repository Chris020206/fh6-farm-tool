from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
import os


LIKELY_FH6_TITLE_TERMS: tuple[str, ...] = (
    "forza horizon 6",
    "fh6",
    "forza horizon",
)


@dataclass(frozen=True)
class WindowCandidate:
    handle: int
    title: str


class FocusHandoffStatus(str, Enum):
    REFUSED_NON_WINDOWS = "refused_non_windows"
    REFUSED_MISSING_CONFIRMATION = "refused_missing_confirmation"
    REFUSED_NO_CANDIDATES = "refused_no_candidates"
    REFUSED_MULTIPLE_CANDIDATES = "refused_multiple_candidates"
    REFUSED_TARGET_NOT_FOUND = "refused_target_not_found"
    REFUSED_DUPLICATE_TARGET_TITLE = "refused_duplicate_target_title"
    FOCUS_SUCCEEDED = "focus_succeeded"
    FOCUS_FAILED = "focus_failed"


@dataclass(frozen=True)
class FocusHandoffResult:
    status: FocusHandoffStatus
    message: str
    candidates: tuple[WindowCandidate, ...] = ()
    selected_candidate: WindowCandidate | None = None
    focus_attempted: bool = False

    @property
    def succeeded(self) -> bool:
        return self.status == FocusHandoffStatus.FOCUS_SUCCEEDED


WindowProvider = Callable[[], tuple[WindowCandidate, ...]]
FocusProvider = Callable[[WindowCandidate], bool]


def title_matches_fh6(title: str) -> bool:
    normalized_title = title.strip().lower()
    return any(term in normalized_title for term in LIKELY_FH6_TITLE_TERMS)


def filter_fh6_window_candidates(
    windows: tuple[WindowCandidate, ...],
) -> tuple[WindowCandidate, ...]:
    return tuple(candidate for candidate in windows if title_matches_fh6(candidate.title))


def select_focus_candidate(
    candidates: tuple[WindowCandidate, ...],
    exact_title: str | None = None,
) -> WindowCandidate | None:
    if exact_title is not None:
        normalized_exact_title = exact_title.strip().lower()
        exact_matches = tuple(
            candidate
            for candidate in candidates
            if candidate.title.strip().lower() == normalized_exact_title
        )
        if len(exact_matches) == 1:
            return exact_matches[0]
        return None

    if len(candidates) == 1:
        return candidates[0]

    return None


def find_exact_title_matches(
    candidates: tuple[WindowCandidate, ...],
    exact_title: str,
) -> tuple[WindowCandidate, ...]:
    normalized_exact_title = exact_title.strip().lower()
    return tuple(
        candidate
        for candidate in candidates
        if candidate.title.strip().lower() == normalized_exact_title
    )


def attempt_fh6_focus_handoff(
    confirm_focus: bool,
    exact_title: str | None = None,
    os_name: str | None = None,
    window_provider: WindowProvider | None = None,
    focus_provider: FocusProvider | None = None,
) -> FocusHandoffResult:
    current_os_name = os_name or os.name
    if current_os_name != "nt":
        return FocusHandoffResult(
            status=FocusHandoffStatus.REFUSED_NON_WINDOWS,
            message="Focus handoff is only available on Windows.",
        )

    provider = window_provider or list_visible_windows
    candidates = filter_fh6_window_candidates(provider())

    if not candidates:
        return FocusHandoffResult(
            status=FocusHandoffStatus.REFUSED_NO_CANDIDATES,
            message="No likely FH6 window was found.",
            candidates=candidates,
        )

    if exact_title is not None:
        exact_matches = find_exact_title_matches(
            candidates=candidates,
            exact_title=exact_title,
        )
        if not exact_matches:
            return FocusHandoffResult(
                status=FocusHandoffStatus.REFUSED_TARGET_NOT_FOUND,
                message="No likely FH6 window matched the exact target title.",
                candidates=candidates,
            )
        if len(exact_matches) > 1:
            return FocusHandoffResult(
                status=FocusHandoffStatus.REFUSED_DUPLICATE_TARGET_TITLE,
                message="Multiple FH6 windows matched the exact target title.",
                candidates=candidates,
            )

    selected_candidate = select_focus_candidate(
        candidates=candidates,
        exact_title=exact_title,
    )
    if selected_candidate is None:
        return FocusHandoffResult(
            status=FocusHandoffStatus.REFUSED_MULTIPLE_CANDIDATES,
            message=(
                "Multiple likely FH6 windows were found. Provide an exact target title "
                "before attempting focus."
            ),
            candidates=candidates,
        )

    if not confirm_focus:
        return FocusHandoffResult(
            status=FocusHandoffStatus.REFUSED_MISSING_CONFIRMATION,
            message="Focus handoff was not attempted because confirmation was missing.",
            candidates=candidates,
            selected_candidate=selected_candidate,
        )

    focus = focus_provider or focus_window_candidate
    focus_succeeded = focus(selected_candidate)
    if focus_succeeded:
        return FocusHandoffResult(
            status=FocusHandoffStatus.FOCUS_SUCCEEDED,
            message="Focus handoff appeared to succeed.",
            candidates=candidates,
            selected_candidate=selected_candidate,
            focus_attempted=True,
        )

    return FocusHandoffResult(
        status=FocusHandoffStatus.FOCUS_FAILED,
        message="Focus handoff was attempted, but success could not be confirmed.",
        candidates=candidates,
        selected_candidate=selected_candidate,
        focus_attempted=True,
    )


def list_visible_windows() -> tuple[WindowCandidate, ...]:
    if os.name != "nt":
        return ()

    import ctypes

    user32 = ctypes.windll.user32
    candidates: list[WindowCandidate] = []

    enum_windows_proc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

    def collect_window(hwnd, _lparam) -> bool:
        if not user32.IsWindowVisible(hwnd):
            return True

        length = user32.GetWindowTextLengthW(hwnd)
        if length == 0:
            return True

        buffer = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buffer, length + 1)
        title = buffer.value.strip()
        if title:
            candidates.append(WindowCandidate(handle=int(hwnd), title=title))

        return True

    user32.EnumWindows(enum_windows_proc(collect_window), 0)
    return tuple(candidates)


def focus_window_candidate(candidate: WindowCandidate) -> bool:
    if os.name != "nt":
        return False

    import ctypes

    user32 = ctypes.windll.user32
    hwnd = candidate.handle
    sw_restore = 9

    if user32.IsIconic(hwnd):
        user32.ShowWindow(hwnd, sw_restore)

    user32.SetForegroundWindow(hwnd)
    return int(user32.GetForegroundWindow()) == hwnd
