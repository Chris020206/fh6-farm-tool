"""Desktop execution availability boundaries."""

SUPPORTED_DESKTOP_AUTOMATION_IDS = frozenset({"auto1", "auto2", "auto3"})


def is_desktop_execution_supported(automation_id: str) -> bool:
    return automation_id in SUPPORTED_DESKTOP_AUTOMATION_IDS


def is_desktop_preparation_available(automation_id: str) -> bool:
    return automation_id in SUPPORTED_DESKTOP_AUTOMATION_IDS

