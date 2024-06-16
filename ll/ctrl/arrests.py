from pygame import Rect, Vector2 as V2
from dataclasses import dataclass
from typing import Callable

from any.locales import kames
from any.pictures import IMG_HAZURE
from model.kard import Kard
from model.player import Player
from ptc.bridge import Bridge
from view.arrest.bind_mv import bind_mv
from view.arrest.engage_mv import engage_mv
from view.arrest.face_up_mv import face_up_mv
from view.arrest.hazure_mv import hazure_mv
from view.message_view import MessageView

_Rect = Rect(200, 120, 880, 480)
_Huda = V2(340, 475)

@dataclass
class ArrestsController():
    injector: Callable[[], Bridge]

    @property
    def bridge(self) -> Bridge:
        return self.injector()

    def action(self, player: Player, kard: Kard) -> None:
        self.bridge.whileloop(new_view=engage_mv(
            bridge=self.bridge,
            rect=_Rect,
            kard=kard
        ))
        pk = player.hands[0]
        self.bridge.whileloop(new_view=face_up_mv(
            bridge=self.bridge,
            rect=_Rect,
            kard=kard,
            img_after=pk.picture() if pk == kard else IMG_HAZURE
        ))
        if pk == kard:
            self.bridge.whileloop(new_view=bind_mv(
                bridge=self.bridge,
                rect=_Rect,
                kard=kard,
                img_actor=pk.picture()
            ))
            self.bridge.whileloop(new_view=MessageView(
                view=self.bridge.view,
                img_mes=kames(folder="heisi", key="arrests", player_name=player.name)
            ))
        else:
            self.bridge.whileloop(new_view=hazure_mv(
                bridge=self.bridge,
                rect=_Rect,
                kard=kard
            ))
