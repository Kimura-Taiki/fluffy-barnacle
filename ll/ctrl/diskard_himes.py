from dataclasses import dataclass
from typing import Callable

from any.locales import kames
from model.player import Player
from ptc.bridge import Bridge
from view.message_view import MessageView

@dataclass
class DiskardHimesController():
    injector: Callable[[], Bridge]

    @property
    def bridge(self) -> Bridge:
        return self.injector()

    def action(self, player: Player) -> None:
        self.bridge.whileloop(new_view=MessageView(
            view=self.bridge.view,
            img_mes=kames(folder="hime", key="diskard_himes", player_name=player.name)
        ))
