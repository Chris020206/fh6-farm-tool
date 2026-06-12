from dataclasses import dataclass


@dataclass(frozen=True)
class InputResult:
    action_name: str
    key_name: str | None
    changed: bool
    message: str
