from dataclasses import dataclass

from core.input import InputResult
from core.sequence import SequenceResult


@dataclass(frozen=True)
class Auto2RunResult:
    status: str
    message: str
    sequence_result: SequenceResult | None = None
    cleanup_result: InputResult | None = None

    @property
    def completed(self) -> bool:
        return self.status == "completed"

    @property
    def stopped(self) -> bool:
        return self.status == "stopped"

    @property
    def failed(self) -> bool:
        return self.status == "failed"


@dataclass(frozen=True)
class Auto2LoopResult:
    status: str
    requested_cycles: int
    completed_cycles: int
    message: str
    last_cycle_result: Auto2RunResult | None = None
    cleanup_result: InputResult | None = None

    @property
    def completed(self) -> bool:
        return self.status == "completed"

    @property
    def stopped(self) -> bool:
        return self.status == "stopped"

    @property
    def failed(self) -> bool:
        return self.status == "failed"
