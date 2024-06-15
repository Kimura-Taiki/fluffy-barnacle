from pygame import Rect, Vector2 as V2
from dataclasses import dataclass
from typing import Callable

from model.player import Player
from ptc.bridge import Bridge
from view.duel.engage_mv import engage_mv
from view.duel.face_up_mv import face_up_mv
from view.duel.slash_mv import slash_mv
from view.duel.result_mv import result_mv

_Rect = Rect(200, 120, 880, 480)
_Huda = V2(340, 475)

from ptc.controller import Controller
@dataclass
class DuelsController():
    injector: Callable[[], Bridge]

    @property
    def bridge(self) -> Bridge:
        return self.injector()

    def action(self, p1: Player, p2: Player) -> None:
        self.bridge.whileloop(new_view=engage_mv(
            bridge=self.bridge,
            rect=_Rect,
        ))
        self.bridge.whileloop(new_view=face_up_mv(
            bridge=self.bridge,
            rect=_Rect,
            k1=p1.hands[0],
            k2=p2.hands[0]
        ))
        self.bridge.whileloop(new_view=slash_mv(
            bridge=self.bridge,
            rect=_Rect,
            k1=p1.hands[0],
            k2=p2.hands[0]
        ))
        if p1.hand.rank != p2.hand.rank:
            self.bridge.whileloop(new_view=result_mv(
                bridge=self.bridge,
                rect=_Rect,
                p1=p1,
                p2=p2
            ))
        