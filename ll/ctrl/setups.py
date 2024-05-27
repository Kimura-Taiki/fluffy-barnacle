from pygame import Vector2 as V2

from ctrl.draw_kards import DrawKardsController
from model.kard import EMPTY_KARD
from ptc.bridge import Bridge
from view.board_view import BoardView
from view.deck_square import DeckSquare
from view.player_square import PlayerSquare
from view.draw_view import DrawView

from ptc.controller import Controller
class SetupsController():
    # def __init__(self, bridge: Bridge, deck_square: DeckSquare, player_square: PlayerSquare) -> None:
    def __init__(self, bridge: Bridge) -> None:
        self.bridge = bridge
        # self.deck_square = deck_square
        # self.player_square = player_square

    def action(self) -> None:
        handless_player = next((player for player in self.bridge.board.players if player.hand == EMPTY_KARD), None)
        view = self.bridge.view
        if not isinstance(view, BoardView):
            raise ValueError("SetupsControllerを起動する時はBoardViewでないと")
        if handless_player:
            view.draw_kard_action(
                player=handless_player,
                suffix=self._draw_suffix
            )
        else:
            self._game_start()

    def _draw_suffix(self) -> None:
        self.action()

    def _game_start(self) -> None:
        raise EOFError("良し！")
