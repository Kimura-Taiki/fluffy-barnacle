from any.font import MS_MINCHO_COL
from ctrl.draw_kards import DrawKardsController
from ptc.bridge import Bridge
from view.board_view import BoardView
from view.message_view import MessageView

_FONT_H = 96

from ptc.controller import Controller
class TurnStartsController():
    def __init__(self, bridge: Bridge) -> None:
        self.bridge = bridge

    def action(self) -> None:
        view = self.bridge.view
        if not isinstance(view, BoardView):
            raise ValueError("TurnStartsControllerを起動する時はBoardViewでないと")
        self._old_view = self.bridge.view
        self.bridge.view = MessageView(
            board_view=view,
            img_mes=MS_MINCHO_COL(f"{self.bridge.board.turn_player.name}'s Turn", _FONT_H, "black"),
            callback=self._draw_callback
        )

    def _draw_callback(self) -> None:
        self.bridge.view = self._old_view
        view = self.bridge.view
        if not isinstance(view, BoardView):
            raise ValueError("TurnStartsControllerを起動する時はBoardViewでないと")
        DrawKardsController(
            bridge=self.bridge,
            board_view=view,
            player=self.bridge.board.turn_player,
            suffix=self._suffix
        ).action()

    def _suffix(self) -> None:
        ...
