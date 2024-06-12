from dataclasses import dataclass
from typing import Callable, Any
# from model.board import Board
from model.player import Player
from ptc.bridge import Bridge

@dataclass(frozen=True)
class KardCore():
    name: str
    rank: int
    use_func: Callable[[Bridge, Player], None] = lambda bridge, player: None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, KardCore):
            return False
        return self.name == other.name and self.rank == other.rank
