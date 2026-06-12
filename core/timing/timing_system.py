from collections.abc import Callable
from time import monotonic, sleep

from core.timing.timing_result import TimingResult


class TimingSystem:
    def __init__(self, tick_interval_seconds: float = 0.1):
        self.tick_interval_seconds = tick_interval_seconds

    def wait(
        self,
        duration_seconds: float,
        should_cancel: Callable[[], bool] | None = None,
    ) -> TimingResult:
        return self._run_timer(duration_seconds, should_cancel=should_cancel)

    def countdown(
        self,
        duration_seconds: float,
        on_tick: Callable[[float], None] | None = None,
        should_cancel: Callable[[], bool] | None = None,
    ) -> TimingResult:
        return self._run_timer(
            duration_seconds,
            on_tick=on_tick,
            should_cancel=should_cancel,
        )

    def _run_timer(
        self,
        duration_seconds: float,
        on_tick: Callable[[float], None] | None = None,
        should_cancel: Callable[[], bool] | None = None,
    ) -> TimingResult:
        safe_duration_seconds = max(0.0, duration_seconds)
        start_time = monotonic()
        end_time = start_time + safe_duration_seconds

        while True:
            elapsed_seconds = monotonic() - start_time

            if should_cancel is not None and should_cancel():
                return TimingResult(
                    completed=False,
                    cancelled=True,
                    elapsed_seconds=elapsed_seconds,
                )

            remaining_seconds = max(0.0, end_time - monotonic())
            if on_tick is not None:
                on_tick(remaining_seconds)

            if remaining_seconds <= 0.0:
                return TimingResult(
                    completed=True,
                    cancelled=False,
                    elapsed_seconds=monotonic() - start_time,
                )

            sleep(min(self.tick_interval_seconds, remaining_seconds))
