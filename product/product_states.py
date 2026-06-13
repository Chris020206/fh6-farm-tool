from enum import Enum


class ProductState(str, Enum):
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    STOPPED = "stopped"
    INTERRUPTED = "interrupted"
    REFUSED = "refused"
    WARNING = "warning"
    FOCUS_UNCERTAIN = "focus_uncertain"
    FAILURE = "failure"
