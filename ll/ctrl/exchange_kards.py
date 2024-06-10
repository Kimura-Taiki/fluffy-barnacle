from any.func import enforce
from any.screen import screen
from model.player import Player
from ptc.bridge import Bridge
from view.board_view import BoardView
from view.transition.linear_transition import LinearTransition
from view.moves_view import MovesView
from view.player_square import PlayerSquare

class ExchangeKardsController():
    def __init__(self, bridge: Bridge) -> None:
        self.bridge = bridge
        self.board_view = enforce(bridge.view, BoardView)
        self.img_back = self.board_view.deck_square.img_back

    def action(self, p1: Player, p2: Player) -> None:
        p1_v2 = PlayerSquare.search_v2_by_player(
            squares=self.board_view.squares,
            player=p1,
        )
        p2_v2 = PlayerSquare.search_v2_by_player(
            squares=self.board_view.squares,
            player=p2
        )
        self.bridge.whileloop(new_view=MovesView(
            view=self.bridge.view,
            transitions=[
                LinearTransition(
                    img_actor=self.img_back,
                    from_v2=f,
                    to_v2=t,
                    canvas=screen
                )
                for f, t in [(p1_v2, p2_v2), (p2_v2, p1_v2)]
            ]
        ))
