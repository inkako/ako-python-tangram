from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Principal:
    user_id: Any
    user: Any = None
    is_superuser: bool = False
