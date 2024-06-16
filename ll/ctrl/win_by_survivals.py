from dataclasses import dataclass
from typing import Callable

from any.locales import lomes
from model.player import Player
from ptc.bridge import Bridge
from view.message_view import MessageView

from ptc.controller import Controller
@dataclass
class WinBySurvivalsController():
    injector: Callable[[], Bridge]

    @property
    def bridge(self) -> Bridge:
        return self.injector()

    def action(self, player: Player) -> None:
        self.bridge.whileloop(new_view=MessageView(
            view=self.bridge.view,
            img_mes=lomes(folder="board", key="win_by_survivals", player_name=player.name)
        ))
