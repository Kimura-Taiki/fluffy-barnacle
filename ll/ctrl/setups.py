from ctrl.draw_kards import DrawKardsController
from ctrl.turn_starts import TurnStartsController
from ptc.bridge import Bridge

from ptc.controller import Controller
class SetupsController():
    def __init__(self, bridge: Bridge) -> None:
        self.bridge = bridge

    def action(self) -> None:
        while (handless_player := next((
            player for player in self.bridge.board.players if len(player.hands) == 0
        ), None)):
            DrawKardsController(
                bridge=self.bridge,
                board_view=self.bridge.view,
                player=handless_player,
            ).action()
        else:
            self._game_start()

    def _game_start(self) -> None:
        self.bridge.board.game_start()
        TurnStartsController(bridge=self.bridge).action()
