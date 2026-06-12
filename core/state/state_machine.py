from app_logging.log_manager import get_logger
from core.state.automation_state import AutomationState
from core.state.state_transition_result import StateTransitionResult


class StateMachine:
    _LEGAL_TRANSITIONS = {
        AutomationState.IDLE: {AutomationState.RUNNING},
        AutomationState.RUNNING: {
            AutomationState.STOPPING,
            AutomationState.COMPLETED,
            AutomationState.ERROR,
        },
        AutomationState.STOPPING: {AutomationState.IDLE},
        AutomationState.COMPLETED: {AutomationState.IDLE},
        AutomationState.ERROR: {AutomationState.IDLE},
    }

    def __init__(self) -> None:
        self.current_state = AutomationState.IDLE
        self._logger = get_logger()

    def transition_to(self, new_state: AutomationState) -> StateTransitionResult:
        previous_state = self.current_state
        legal_next_states = self._LEGAL_TRANSITIONS[previous_state]

        if new_state not in legal_next_states:
            message = (
                f"Rejected transition from {previous_state.value} "
                f"to {new_state.value}."
            )
            self._logger.warning(message, category="state")

            return StateTransitionResult(
                accepted=False,
                previous_state=previous_state,
                current_state=self.current_state,
                message=message,
            )

        self.current_state = new_state
        message = f"Transitioned from {previous_state.value} to {new_state.value}."
        self._logger.info(message, category="state")

        return StateTransitionResult(
            accepted=True,
            previous_state=previous_state,
            current_state=self.current_state,
            message=message,
        )
