from pygame import Vector2 as V2

from any.func import enforce
from any.screen import screen
from model.player import Player
from ptc.bridge import Bridge
from view.board_view import BoardView
from view.linear_transition import LinearTransition
from view.moves_view import MovesView
from view.player_square import PlayerSquare

from ptc.controller import Controller
class DrawKardsController():
    def __init__(
            self,
            bridge: Bridge,
        ) -> None:
        self.bridge = bridge
        self.board_view = enforce(bridge.view, BoardView)
        dq = self.board_view.deck_square
        self.img_back = dq.img_back
        self.from_v2 = V2(dq.rect.center)

    def action(self, player: Player) -> None:
        to_v2 = PlayerSquare.search_v2_by_player(
            squares=self.board_view.squares,
            player=player
        )
        self.bridge.whileloop(new_view=MovesView(
            view=self.bridge.view,
            transitions=[LinearTransition(
                img_actor=self.img_back,
                from_v2=self.from_v2,
                to_v2=to_v2,
                canvas=screen
            )]
        ))
