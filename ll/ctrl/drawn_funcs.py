from dataclasses import dataclass
from typing import Callable

from model.kard import Kard
from model.player import Player
from ptc.bridge import Bridge

from ptc.controller import Controller
@dataclass
class DrawnFuncsController():
    injector: Callable[[], Bridge]

    @property
    def bridge(self) -> Bridge:
        return self.injector()

    def action(self, player: Player, kard: Kard) -> None:
        for pk in player.hands:
            pk.drawn_func(bridge=self.bridge, player=player)