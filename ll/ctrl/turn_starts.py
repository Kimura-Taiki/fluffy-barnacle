from any.font import MS_MINCHO_COL
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
            img_mes=MS_MINCHO_COL(f"{self.bridge.board.turn_player.name}'s Turn", _FONT_H, "black"),
        ))
