from dataclasses import dataclass, field


@dataclass(frozen=True)
class BaseAction:
    action_type: str = field(init=False)
