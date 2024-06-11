from dataclasses import dataclass
from typing import Callable, Any
from model.board import Board

@dataclass(frozen=True)
class KardCore():
    name: str
    rank: int
    func: Callable[[Board], None] = lambda board: None