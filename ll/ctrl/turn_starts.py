from model.kard import EMPTY_KARD
from ptc.bridge import Bridge
from view.board_view import BoardView

from ptc.controller import Controller
class TurnStartsController():
    def __init__(self, bridge: Bridge) -> None:
        self.bridge = bridge

    def action(self) -> None:
        view = self.bridge.view
        if not isinstance(view, BoardView):
            raise ValueError("TurnStartsControllerを起動する時はBoardViewでないと")
        view.draw_kard_action(
            player=self.bridge.board.turn_player,
            suffix=self._suffix
        )()

    def _suffix(self) -> None:
        print(self.bridge.board)