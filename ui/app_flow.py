from dataclasses import dataclass
from enum import Enum


class AppFlowState(str, Enum):
    HOME = "home"
    AUTOMATION_ENVIRONMENT = "automation_environment"
    PREPARED = "prepared"
    RUNNING = "running"
    COMPANION_MODE = "companion_mode"
    COMPLETED = "completed"
    STOPPED = "stopped"
    INTERRUPTED = "interrupted"
    REFUSED = "refused"


class AppFlowTrigger(str, Enum):
    SELECT_AUTOMATION = "select_automation"
    PREPARE_REQUEST = "prepare_request"
    OPERATOR_COMMITMENT = "operator_commitment"
    ENTER_COMPANION_MODE = "enter_companion_mode"
    EXPAND_RUNNING_VIEW = "expand_running_view"
    MARK_COMPLETED = "mark_completed"
    MARK_STOPPED = "mark_stopped"
    MARK_INTERRUPTED = "mark_interrupted"
    HANDLE_REFUSAL = "handle_refusal"
    REVIEW_REFUSAL = "review_refusal"
    REVIEW_HISTORY = "review_history"
    RETURN_HOME = "return_home"
    RETURN_AUTOMATION_ENVIRONMENT = "return_automation_environment"


@dataclass(frozen=True)
class AppFlowTransition:
    from_state: AppFlowState
    to_state: AppFlowState
    trigger: AppFlowTrigger
    user_intent: str
    product_meaning: str
    recovery_path: str | None = None
    is_companion_transition: bool = False


@dataclass(frozen=True)
class AppFlow:
    transitions: tuple[AppFlowTransition, ...]

    def available_transitions(
        self,
        from_state: AppFlowState,
    ) -> tuple[AppFlowTransition, ...]:
        return tuple(
            transition
            for transition in self.transitions
            if transition.from_state == from_state
        )

    def can_transition(
        self,
        from_state: AppFlowState,
        to_state: AppFlowState,
    ) -> bool:
        return any(
            transition.from_state == from_state and transition.to_state == to_state
            for transition in self.transitions
        )


APP_FLOW_TRANSITIONS: tuple[AppFlowTransition, ...] = (
    AppFlowTransition(
        from_state=AppFlowState.HOME,
        to_state=AppFlowState.AUTOMATION_ENVIRONMENT,
        trigger=AppFlowTrigger.SELECT_AUTOMATION,
        user_intent="Choose an automation to understand and prepare.",
        product_meaning="Move from broad orientation to automation-specific confidence formation.",
    ),
    AppFlowTransition(
        from_state=AppFlowState.AUTOMATION_ENVIRONMENT,
        to_state=AppFlowState.PREPARED,
        trigger=AppFlowTrigger.PREPARE_REQUEST,
        user_intent="Prepare a safe product-facing run plan.",
        product_meaning="Readiness, profile, warnings, and request shape are available for review.",
    ),
    AppFlowTransition(
        from_state=AppFlowState.PREPARED,
        to_state=AppFlowState.RUNNING,
        trigger=AppFlowTrigger.OPERATOR_COMMITMENT,
        user_intent="Commit to a prepared run through the future mediated execution path.",
        product_meaning="The app transitions from confidence formation to supervised running state.",
    ),
    AppFlowTransition(
        from_state=AppFlowState.RUNNING,
        to_state=AppFlowState.COMPANION_MODE,
        trigger=AppFlowTrigger.ENTER_COMPANION_MODE,
        user_intent="Reduce the app to peripheral running awareness.",
        product_meaning="Companion mode is available only while automation is running.",
        is_companion_transition=True,
    ),
    AppFlowTransition(
        from_state=AppFlowState.COMPANION_MODE,
        to_state=AppFlowState.RUNNING,
        trigger=AppFlowTrigger.EXPAND_RUNNING_VIEW,
        user_intent="Return from reduced companion awareness to the running view.",
        product_meaning="The running state remains the source of truth for companion mode.",
        is_companion_transition=True,
    ),
    AppFlowTransition(
        from_state=AppFlowState.RUNNING,
        to_state=AppFlowState.COMPLETED,
        trigger=AppFlowTrigger.MARK_COMPLETED,
        user_intent="Understand that the run ended as expected.",
        product_meaning="Completion should lead to quiet reassurance and next-step clarity.",
        recovery_path="Review summary, then return Home or prepare another automation run.",
    ),
    AppFlowTransition(
        from_state=AppFlowState.RUNNING,
        to_state=AppFlowState.STOPPED,
        trigger=AppFlowTrigger.MARK_STOPPED,
        user_intent="Understand that the operator stopped execution intentionally.",
        product_meaning="Stopped state should feel controlled, not failed.",
        recovery_path="Review baseline state, then return to the Automation Environment or Home.",
    ),
    AppFlowTransition(
        from_state=AppFlowState.RUNNING,
        to_state=AppFlowState.INTERRUPTED,
        trigger=AppFlowTrigger.MARK_INTERRUPTED,
        user_intent="Recover calmly after execution did not complete.",
        product_meaning="Interruption should guide review before another commitment.",
        recovery_path="Review FH6 baseline and session notes before preparing another run.",
    ),
    AppFlowTransition(
        from_state=AppFlowState.AUTOMATION_ENVIRONMENT,
        to_state=AppFlowState.REFUSED,
        trigger=AppFlowTrigger.HANDLE_REFUSAL,
        user_intent="Understand why a request was blocked before execution.",
        product_meaning="Refused means protective clarity, not execution failure.",
        recovery_path="Resolve the refusal condition and return to the Automation Environment.",
    ),
    AppFlowTransition(
        from_state=AppFlowState.REFUSED,
        to_state=AppFlowState.AUTOMATION_ENVIRONMENT,
        trigger=AppFlowTrigger.REVIEW_REFUSAL,
        user_intent="Return to the preparation surface after reviewing refusal guidance.",
        product_meaning="The operator can correct the request without mode shock.",
    ),
    AppFlowTransition(
        from_state=AppFlowState.COMPLETED,
        to_state=AppFlowState.AUTOMATION_ENVIRONMENT,
        trigger=AppFlowTrigger.RETURN_AUTOMATION_ENVIRONMENT,
        user_intent="Prepare another run after reviewing completion.",
        product_meaning="Completion can flow back into confidence formation.",
    ),
    AppFlowTransition(
        from_state=AppFlowState.STOPPED,
        to_state=AppFlowState.AUTOMATION_ENVIRONMENT,
        trigger=AppFlowTrigger.RETURN_AUTOMATION_ENVIRONMENT,
        user_intent="Review assumptions before preparing another run.",
        product_meaning="Stopped state returns through preparation, not direct execution.",
    ),
    AppFlowTransition(
        from_state=AppFlowState.INTERRUPTED,
        to_state=AppFlowState.AUTOMATION_ENVIRONMENT,
        trigger=AppFlowTrigger.RETURN_AUTOMATION_ENVIRONMENT,
        user_intent="Recover through readiness review before another run.",
        product_meaning="Interrupted state requires renewed confidence formation.",
    ),
    AppFlowTransition(
        from_state=AppFlowState.COMPLETED,
        to_state=AppFlowState.HOME,
        trigger=AppFlowTrigger.RETURN_HOME,
        user_intent="Return to broad orientation after a completed run.",
        product_meaning="The operator can leave the run context without losing continuity.",
    ),
    AppFlowTransition(
        from_state=AppFlowState.STOPPED,
        to_state=AppFlowState.HOME,
        trigger=AppFlowTrigger.RETURN_HOME,
        user_intent="Return to broad orientation after a controlled stop.",
        product_meaning="Stopped state remains calm and recoverable.",
    ),
    AppFlowTransition(
        from_state=AppFlowState.INTERRUPTED,
        to_state=AppFlowState.HOME,
        trigger=AppFlowTrigger.RETURN_HOME,
        user_intent="Return to broad orientation after reviewing interruption.",
        product_meaning="Interruption recovery can safely leave the automation context.",
    ),
)


APP_FLOW = AppFlow(transitions=APP_FLOW_TRANSITIONS)


def get_app_flow() -> AppFlow:
    return APP_FLOW
