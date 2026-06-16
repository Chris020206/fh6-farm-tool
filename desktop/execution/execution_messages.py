"""Shared desktop execution messages and result mapping."""


def desktop_execution_refusal_details(automation_id: str) -> tuple[str, ...]:
    if automation_id == "auto2":
        return (
            "Auto2 is available through the guarded desktop flow.",
            "Test navigation and finite purchase modes remain bounded.",
            "F8 stop is registered by the guarded Auto2 runner.",
        )

    if automation_id == "auto3":
        return (
            "Auto3 is available through the guarded desktop flow.",
            "Traversal and unlock modes remain bounded to the validated car limit.",
            "F8 stop is registered by the guarded Auto3 runner.",
        )

    return (
        "Desktop execution is not available for this automation.",
        "No operation will start from this UI path.",
    )


def desktop_execution_confirmation_summary(automation_id: str) -> str:
    if automation_id == "auto1":
        return "Desktop path uses focus handoff, countdown, F8 stop, and guarded Auto1 cleanup."

    if automation_id == "auto2":
        return "Desktop path uses focus handoff, countdown, F8 stop, and guarded Auto2 bounded execution."

    if automation_id == "auto3":
        return "Desktop path uses focus handoff, countdown, F8 stop, and guarded Auto3 bounded execution."

    return "Execution is unavailable from the desktop UI."


def completion_state_id_for_status(status: str) -> str:
    if status == "completed":
        return "completed"

    if status == "stopped":
        return "stopped"

    return "refused"


def completion_state_id_for_auto1_status(status: str) -> str:
    return completion_state_id_for_status(status)


def summarize_ui_execution_error(automation_label: str, error: Exception) -> str:
    message = str(error).strip() or error.__class__.__name__
    return f"{automation_label} guarded run unavailable: {error.__class__.__name__}: {message}"


def summarize_auto1_ui_execution_error(error: Exception) -> str:
    return summarize_ui_execution_error("Auto1", error)

