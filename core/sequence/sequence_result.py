from dataclasses import dataclass

from core.stop.stop_result import StopResult


@dataclass(frozen=True)
class SequenceResult:
    completed: bool
    stopped: bool
    actions_executed: int
    message: str
    stop_result: StopResult | None = None
