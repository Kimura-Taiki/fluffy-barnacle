from pygame import Vector2 as V2

from model.player import Player
from ptc.bridge import Bridge
from ptc.view import View
from view.board_view import BoardView
from view.linear_view import LinearView
from view.player_square import PlayerSquare

from ptc.controller import Controller
class DrawKardsController():
    def __init__(
            self,
            bridge: Bridge,
            board_view: View,
            player: Player,
        ) -> None:
        self.bridge = bridge
        if not isinstance(board_view, BoardView):
            raise ValueError("DrawKardsController を起動する時はBoardViewでないと", board_view)
        self.board_view = board_view
        self.player = player
        dq = board_view.deck_square
        self.img_back = dq.img_back
        self.from_v2 = V2(dq.rect.center)
        self.to_v2 = PlayerSquare.search_v2_by_player(
            squares=self.board_view.squares,
            player=player
        )

    def action(self) -> None:
        self.bridge.whileloop(new_view=LinearView(
            view=self.bridge.view,
            img_back=self.img_back,
            from_v2=self.from_v2,
            to_v2=self.to_v2,
        ))
        self.bridge.board.draw(player=self.player)
