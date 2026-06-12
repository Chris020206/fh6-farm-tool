from dataclasses import dataclass

from core.input.input_result import InputResult


@dataclass(frozen=True)
class StopResult:
    stop_requested: bool
    cleanup_result: InputResult | None
    message: str
