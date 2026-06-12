from dataclasses import dataclass, field

from core.actions.base_action import BaseAction


@dataclass(frozen=True)
class KeyPressAction(BaseAction):
    key: str
    action_type: str = field(default="key_press", init=False)
