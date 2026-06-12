from dataclasses import dataclass, field

from core.actions.base_action import BaseAction


@dataclass(frozen=True)
class KeyReleaseAction(BaseAction):
    key: str
    action_type: str = field(default="key_release", init=False)
