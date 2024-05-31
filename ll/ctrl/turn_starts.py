from any.font import MS_MINCHO_COL
from ctrl.draw_kards import DrawKardsController
from ctrl.messages import MessagesController
from ptc.bridge import Bridge
from view.board_view import BoardView

_FONT_H = 96

from ptc.controller import Controller
class TurnStartsController():
    def __init__(self, bridge: Bridge) -> None:
        self.bridge = bridge

    def action(self) -> None:
        MessagesController(
            bridge=self.bridge,
            img_mes=MS_MINCHO_COL(f"{self.bridge.board.turn_player.name}'s Turn", _FONT_H, "black"),
            suffix=self._suffix
        ).action()

    def _suffix(self) -> None:
        view = self.bridge.view
        if not isinstance(view, BoardView):
            raise ValueError("TurnStartsControllerを起動する時はBoardViewでないと")
        DrawKardsController(
            bridge=self.bridge,
            board_view=view,
            player=self.bridge.board.turn_player,
        ).action()
