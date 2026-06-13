from enum import Enum


class SessionStatus(str, Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    STOPPED = "stopped"
    INTERRUPTED = "interrupted"
    REFUSED = "refused"
    FAILURE = "failure"
