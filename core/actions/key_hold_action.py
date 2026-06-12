from dataclasses import dataclass, field

from core.actions.base_action import BaseAction


@dataclass(frozen=True)
class KeyHoldAction(BaseAction):
    key: str
    duration_seconds: float
    action_type: str = field(default="key_hold", init=False)
