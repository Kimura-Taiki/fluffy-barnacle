from dataclasses import dataclass
from typing import Callable

from any.func import enforce
from any.screen import screen
from model.player import Player
from ptc.bridge import Bridge
from view.board_view import BoardView
from view.moves_view import MovesView
from view.player_square import PlayerSquare
from view.shield_transition import ShieldTransition

from ptc.controller import Controller
@dataclass
class ProtectsController():
    injector: Callable[[], Bridge]

    @property
    def bridge(self) -> Bridge:
        return self.injector()

    def action(self, player: Player) -> None:
        board_view = enforce(self.bridge.view, BoardView)
        to_v2 = PlayerSquare.search_v2_by_player(
            squares=board_view.squares,
            player=player
        )
        self.bridge.whileloop(new_view=MovesView(
            view=self.bridge.view,
            transitions=[ShieldTransition(
                to_v2=to_v2,
                canvas=screen
            )]
        ))
