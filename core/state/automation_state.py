from enum import Enum


class AutomationState(Enum):
    IDLE = "idle"
    RUNNING = "running"
    STOPPING = "stopping"
    ERROR = "error"
    COMPLETED = "completed"
