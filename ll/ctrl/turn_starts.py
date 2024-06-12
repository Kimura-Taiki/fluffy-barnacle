from any.font import MS_MINCHO_COL
from any.locales import lomes
from ptc.bridge import Bridge
from view.message_view import MessageView

_FONT_H = 96

from ptc.controller import Controller
class TurnStartsController():
    def __init__(self, bridge: Bridge) -> None:
        self.bridge = bridge

    def action(self) -> None:
        self.bridge.whileloop(new_view=MessageView(
            view=self.bridge.view,
            img_mes=MS_MINCHO_COL(lomes(
                folder="board", key="turn_starts", turn_player=self.bridge.board.turn_player.name
            ), _FONT_H, "black"),
        ))
