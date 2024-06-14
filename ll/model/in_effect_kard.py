from pygame import Surface
from dataclasses import dataclass
from typing import Any

from model.kard_core import KardCore
from model.kard_picture_cache import kp_cache
from model.player import Player
from ptc.bridge import Bridge

@dataclass(frozen=True)
class InEffectKard():
    kard_core: KardCore
    png_file: str

    def picture(self) -> Surface:
        return kp_cache.picture(key=(self.kard_core, self.png_file))

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

    @property
    def view_hash(self) -> tuple[Any, ...]:
        return (
            self.kard_core.id.value,
            self.png_file
        )
    
    def use_func(self, bridge: Bridge, player: Player) -> None:
        self.kard_core.use_func(bridge, player)