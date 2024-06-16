from dataclasses import dataclass, field
from typing import Callable

from model.effect import Effect
from model.kard_id import KardID
from model.player import Player
from ptc.bridge import Bridge

@dataclass(frozen=True)
class KardCore:
    id: KardID
    name: Callable[[], str]
    rank: int
    use_func: Callable[[Bridge, Player], None] = lambda bridge, player: None
    drawn_func: Callable[[Bridge, Player], None] = lambda bridge, player: None
    discard_func: Callable[[Bridge, Player], None] = lambda bridge, player: None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, KardCore):
            return False
        return self.id == other.id
