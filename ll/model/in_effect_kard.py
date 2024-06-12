from pygame import Surface
from dataclasses import dataclass
from typing import Any

from any.pictures import picload
from model.board import Board
from model.kard_core import KardCore
from model.player import Player
from ptc.bridge import Bridge


@dataclass(frozen=True)
class InEffectKard():
    kard_core: KardCore
    png_file: str

    def picture(self) -> Surface:
        return picload(self.png_file)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, InEffectKard):
            return False
        return self.kard_core == other.kard_core

    @property
    def name(self) -> str:
        return self.kard_core.name
    
    @property
    def rank(self) -> int:
        return self.kard_core.rank
    
    def use_func(self, bridge: Bridge, player: Player) -> None:
        self.kard_core.use_func(bridge, player)