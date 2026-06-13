from enum import Enum


class SessionStatus(str, Enum):
    PREPARED = "prepared"
    RUNNING = "running"
    COMPLETED = "completed"
    STOPPED = "stopped"
    INTERRUPTED = "interrupted"
    REFUSED = "refused"
    FAILURE = "failure"
