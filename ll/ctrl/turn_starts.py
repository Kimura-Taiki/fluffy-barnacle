from any.font import MS_MINCHO_COL
from ctrl.messages import MessagesController
from ptc.bridge import Bridge

_FONT_H = 96

from ptc.controller import Controller
class TurnStartsController():
    def __init__(self, bridge: Bridge) -> None:
        self.bridge = bridge

    def action(self) -> None:
        MessagesController(
            bridge=self.bridge,
            img_mes=MS_MINCHO_COL(f"{self.bridge.board.turn_player.name}'s Turn", _FONT_H, "black"),
        ).action()
        self.bridge.board.draw(player=self.bridge.board.turn_player)
        if not self.bridge.board.turn_player.alive:
            self.bridge.board.advance_to_next_turn()
            TurnStartsController(bridge=self.bridge).action()
