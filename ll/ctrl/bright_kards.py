from dataclasses import dataclass
from typing import Callable

from model.kard import Kard
from model.player import Player
from ptc.bridge import Bridge
from view.use_kard_view import UseKardView

from ptc.controller import Controller
@dataclass
class BrightKardsController():
    injector: Callable[[], Bridge]

    @property
    def bridge(self) -> Bridge:
        return self.injector()

    def action(self, player: Player, kard: Kard) -> None:
        self.bridge.whileloop(new_view=UseKardView(
            view=self.bridge.view,
            kard=kard,
        ))
