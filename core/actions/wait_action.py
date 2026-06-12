from dataclasses import dataclass, field

from core.actions.base_action import BaseAction


@dataclass(frozen=True)
class WaitAction(BaseAction):
    duration_seconds: float
    action_type: str = field(default="wait", init=False)
