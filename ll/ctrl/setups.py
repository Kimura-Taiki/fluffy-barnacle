from ctrl.turn_starts import TurnStartsController
from model.kard import EMPTY_KARD
from ptc.bridge import Bridge
from view.board_view import BoardView

from ptc.controller import Controller
class SetupsController():
    def __init__(self, bridge: Bridge) -> None:
        self.bridge = bridge

    def action(self) -> None:
        handless_player = next((player for player in self.bridge.board.players if player.hand == EMPTY_KARD), None)
        view = self.bridge.view
        if not isinstance(view, BoardView):
            raise ValueError("SetupsControllerを起動する時はBoardViewでないと")
        if handless_player:
            view.draw_kard_action(
                player=handless_player,
                suffix=self._draw_suffix
            )()
        else:
            self._game_start()

    def _draw_suffix(self) -> None:
        self.action()

    def _game_start(self) -> None:
        self.bridge.board = self.bridge.board._replace(
            turn_player=self.bridge.board.players[0]
        )
        TurnStartsController(bridge=self.bridge).action()
