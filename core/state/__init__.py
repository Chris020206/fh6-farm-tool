"""Centralized lifecycle state management."""

from core.state.automation_state import AutomationState
from core.state.state_machine import StateMachine
from core.state.state_transition_result import StateTransitionResult


__all__ = [
    "AutomationState",
    "StateMachine",
    "StateTransitionResult",
]
