from dataclasses import dataclass
from typing import Callable

from any.font import LL_RENDER
from any.locales import lomes
from ptc.bridge import Bridge
from view.message_view import MessageView

_FONT_H = 96

from ptc.controller import Controller
@dataclass
class TurnStartsController():
    injector: Callable[[], Bridge]

    @property
    def bridge(self) -> Bridge:
        return self.injector()

    def action(self) -> None:
        self.bridge.whileloop(new_view=MessageView(
            view=self.bridge.view,
            img_mes=LL_RENDER(lomes(
                folder="board", key="turn_starts", player_name=self.bridge.board.turn_player.name
            ), _FONT_H, "black"),
        ))
