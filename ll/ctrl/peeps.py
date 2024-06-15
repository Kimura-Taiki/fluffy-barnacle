from pygame import Rect, Vector2 as V2
from dataclasses import dataclass
from typing import Callable

from any.func import enforce
from any.locales import kames
from any.pictures import IMG_PEEP
from any.screen import screen, WV2
from model.player import Player
from ptc.bridge import Bridge
from view.board_view import BoardView
from view.transition.linear_transition import LinearTransition
from view.message_view import MessageView
from view.moves_view import MovesView
from view.peep_transition import PeepTransition
from view.player_square import PlayerSquare

@dataclass
class PeepsController():
    injector: Callable[[], Bridge]

    @property
    def bridge(self) -> Bridge:
        return self.injector()

    def action(self, peeper: Player, watched: Player, subject: Player) -> None:
        board_view = enforce(self.bridge.view, BoardView)
        p_v2 = PlayerSquare.search_v2_by_player(
            squares=board_view.squares,
            player=peeper,
        )
        w_v2 = PlayerSquare.search_v2_by_player(
            squares=board_view.squares,
            player=watched,
        )
        self.bridge.whileloop(new_view=MovesView(
            view=self.bridge.view,
            transitions=[LinearTransition(
                img_actor=IMG_PEEP,
                from_v2=p_v2,
                to_v2=w_v2,
                canvas=screen
            )]
        ))
        if peeper == subject:
            self.bridge.whileloop(new_view=MovesView(
                view=self.bridge.view,
                transitions=[PeepTransition(
                    rect=Rect(WV2/2-V2(340, 475)/2, V2(340, 475)),
                    kard=watched.hands[0],
                    canvas=screen,
                )]
            ))
            self.bridge.whileloop(new_view=MessageView(
                view=self.bridge.view,
                img_mes=kames(
                    folder="douke", key="peeps_subjective",
                    watched_name=watched.name, kard_name=watched.hand.name
                )
            ))
        else:
            self.bridge.whileloop(new_view=MessageView(
                view=self.bridge.view,
                img_mes=kames(
                    folder="douke", key="peeps_objective",
                    peeper_name=peeper.name, watched_name=watched.name
                )
            ))
