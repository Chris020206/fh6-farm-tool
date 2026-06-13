import argparse

from integrations.windows_focus_handoff import (
    attempt_fh6_focus_handoff,
    filter_fh6_window_candidates,
    list_visible_windows,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Manual FH6 focus handoff smoke test. This never presses automation keys."
        )
    )
    parser.add_argument(
        "--confirm-focus",
        action="store_true",
        help="Allow the smoke test to attempt focusing the selected FH6 window.",
    )
    parser.add_argument(
        "--target-title",
        help="Exact FH6 window title to focus when multiple likely windows are found.",
    )
    parser.add_argument(
        "--exact-title",
        dest="target_title",
        help=argparse.SUPPRESS,
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    print("FH6 Farm Tool - Focus Handoff Smoke Test")
    print("Mode: manual feasibility spike")
    print("Safety: no automation keys are pressed")
    print()

    candidates = filter_fh6_window_candidates(list_visible_windows())
    if candidates:
        print("Likely FH6 windows:")
        for candidate in candidates:
            print(f"- handle={candidate.handle} title={candidate.title}")
    else:
        print("Likely FH6 windows: none")

    print()

    result = attempt_fh6_focus_handoff(
        confirm_focus=args.confirm_focus,
        exact_title=args.target_title,
        window_provider=lambda: candidates,
    )

    print(f"Status: {result.status.value}")
    print(f"Result: {result.message}")
    if result.selected_candidate is not None:
        print(f"Selected: {result.selected_candidate.title}")

    return 0 if result.succeeded else 1


if __name__ == "__main__":
    raise SystemExit(main())
