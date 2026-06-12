from dataclasses import dataclass


@dataclass(frozen=True)
class TimingResult:
    completed: bool
    cancelled: bool
    elapsed_seconds: float
