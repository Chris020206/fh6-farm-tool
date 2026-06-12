from dataclasses import dataclass

from core.state.automation_state import AutomationState


@dataclass(frozen=True)
class StateTransitionResult:
    accepted: bool
    previous_state: AutomationState
    current_state: AutomationState
    message: str
