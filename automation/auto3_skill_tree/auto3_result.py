from dataclasses import dataclass

from core.input import InputResult
from core.sequence import SequenceResult


@dataclass(frozen=True)
class Auto3RunResult:
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
