from pygame import Surface, Vector2 as V2, transform
from dataclasses import dataclass
from typing import Any

from any.font import LL_RENDER
from any.pictures import picload
from model.board import Board
from model.kard_core import KardCore
from model.player import Player
from ptc.bridge import Bridge

load_count = 0

@dataclass(frozen=True)
class InEffectKard():
    kard_core: KardCore
    png_file: str

    def picture(self) -> Surface:
        global load_count
        load_count += 1
        print("load_count=", load_count)
        img = picload(self.png_file)
        name = self.kard_core.name
        render = LL_RENDER(name(), 54, "black")
        source = transform.rotozoom(surface=render, angle=0.0, scale=min(1.0, 190/render.get_width()))
        img.blit(source=source, dest=V2(220, 55)-V2(source.get_size())/2)
        return img

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, InEffectKard):
            return False
        return self.kard_core == other.kard_core

    @property
    def name(self) -> str:
        return self.kard_core.name()
    
    @property
    def rank(self) -> int:
        return self.kard_core.rank
    
    def use_func(self, bridge: Bridge, player: Player) -> None:
        self.kard_core.use_func(bridge, player)