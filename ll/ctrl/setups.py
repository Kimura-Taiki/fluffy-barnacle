from ctrl.draw_kards import DrawKardsController
from ctrl.turn_starts import TurnStartsController
from ptc.bridge import Bridge
from view.board_view import BoardView

from ptc.controller import Controller
class SetupsController():
    def __init__(self, bridge: Bridge) -> None:
        self.bridge = bridge

    def action(self) -> None:
        handless_player = next((
            player for player in self.bridge.board.players if len(player.hands) == 0
        ), None)
        view = self.bridge.view
        if not isinstance(view, BoardView):
            raise ValueError("SetupsControllerを起動する時はBoardViewでないと")
        if handless_player:
            DrawKardsController(
                bridge=self.bridge,
                board_view=view,
                player=handless_player,
                suffix=self._draw_suffix
            ).action()
        else:
            self._game_start()

    def _draw_suffix(self) -> None:
        self.action()

    def _game_start(self) -> None:
        self.bridge.board.game_start()
        TurnStartsController(bridge=self.bridge).action()
