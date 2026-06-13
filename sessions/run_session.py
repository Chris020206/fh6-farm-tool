from dataclasses import dataclass, field
from datetime import datetime

from sessions.session_status import SessionStatus


@dataclass(frozen=True)
class RunSession:
    session_id: str
    automation_id: str
    profile_id: str
    requested_count: int
    completed_count: int
    status: SessionStatus
    started_at: datetime
    ended_at: datetime | None = None
    warnings_encountered: tuple[str, ...] = field(default_factory=tuple)
    stop_or_interruption_reason: str | None = None
    user_facing_summary: str | None = None
    user_facing_notes: tuple[str, ...] = field(default_factory=tuple)
    suggested_next_step: str | None = None
    technical_reference: str | None = None

    @property
    def duration_seconds(self) -> float | None:
        if self.ended_at is None:
            return None

        return (self.ended_at - self.started_at).total_seconds()
