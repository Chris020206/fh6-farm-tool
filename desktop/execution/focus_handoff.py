"""Desktop FH6 focus handoff helpers."""

DEFAULT_FH6_TARGET_TITLE = "Forza Horizon 6"


def attempt_ui_focus_handoff(companion_state: dict[str, str]):
    from app_logging.log_manager import configure_logging
    from integrations.windows_focus_handoff import attempt_fh6_focus_handoff

    logger = configure_logging()
    logger.warning(
        "UI focus handoff attempt starting. target_title=%s automation=%s",
        DEFAULT_FH6_TARGET_TITLE,
        companion_state.get("automation_id", "unknown"),
        category="state",
    )

    def log_confirmation_attempt(attempt_number, active_candidate) -> None:
        active_title = active_candidate.title if active_candidate is not None else "<none>"
        active_handle = active_candidate.handle if active_candidate is not None else "<none>"
        logger.warning(
            "UI focus handoff confirmation attempt %s active_title=%s active_handle=%s",
            attempt_number,
            active_title,
            active_handle,
            category="state",
        )

    result = attempt_fh6_focus_handoff(
        confirm_focus=True,
        exact_title=DEFAULT_FH6_TARGET_TITLE,
        confirmation_observer=log_confirmation_attempt,
    )
    if result.succeeded:
        logger.warning(
            "UI focus handoff succeeded: %s active_title=%s active_handle=%s",
            result.message,
            result.active_candidate.title if result.active_candidate else "<none>",
            result.active_candidate.handle if result.active_candidate else "<none>",
            category="state",
        )
    else:
        logger.error(
            "UI focus handoff failed closed: %s (%s) target_title=%s active_title=%s active_handle=%s attempts=%s",
            result.message,
            result.status.value,
            DEFAULT_FH6_TARGET_TITLE,
            result.active_candidate.title if result.active_candidate else "<none>",
            result.active_candidate.handle if result.active_candidate else "<none>",
            result.confirmation_attempts,
            category="error",
        )
    return result


def format_ui_focus_failure_message(
    focus_result,
    automation_name: str = "operation",
) -> str:
    active_title = (
        focus_result.active_candidate.title
        if focus_result.active_candidate is not None and focus_result.active_candidate.title
        else "unavailable"
    )
    return (
        f"FH6 focus handoff failed before {automation_name} start. "
        f"Reason: {focus_result.message} "
        f"Target title: {DEFAULT_FH6_TARGET_TITLE}. "
        f"Active window: {active_title}. "
        f"Status: {focus_result.status.value}. "
        f"Confirmation attempts: {focus_result.confirmation_attempts}."
    )

