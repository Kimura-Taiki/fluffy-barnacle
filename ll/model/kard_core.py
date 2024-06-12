from dataclasses import dataclass
from typing import Callable
from model.kard_id import KardID
from model.player import Player
from ptc.bridge import Bridge

@dataclass(frozen=True)
class KardCore:
    id: KardID
    # name: Callable[[], str]
    name: str
    rank: int
    use_func: Callable[[Bridge, Player], None] = lambda bridge, player: None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, KardCore):
            return False
        return self.id == other.id
