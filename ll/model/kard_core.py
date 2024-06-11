from dataclasses import dataclass
from typing import Callable, Any
from model.board import Board
from model.player import Player

@dataclass(frozen=True)
class KardCore():
    name: str
    rank: int
    use_func: Callable[[Board, Player], None] = lambda board, player: print("heei!")

    # def use_func(self, board: Board, player: Player) -> None:
    #     print(f"{player.name}が「{self.name}」を使ったよ")
