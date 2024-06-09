from pygame import Rect, Vector2 as V2

from any.pictures import IMG_HAZURE
from model.kard import Kard
from model.player import Player
from ptc.bridge import Bridge
from view.arrest.engage_mv import engage_mv
from view.arrest.face_up_mv import face_up_mv
# from view.linear_transition import LinearTransition
# from view.transition.zoom_transition import ZoomTransitions
# from view.arrest.engage_transition import EngageTransition
# from view.arrest.open_transition import OpenTransition
# from view.arrest.slash_transition import SlashTransition
from view.moves_view import MovesView

_Rect = Rect(200, 120, 880, 480)
_Huda = V2(340, 475)

class ArrestsController():
    def __init__(self, bridge: Bridge) -> None:
        self.bridge = bridge

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


        # self.bridge.whileloop(new_view=MovesView(
        #     view=self.bridge.view,
        #     transitions=[DuelOpenTransition(
        #         rect=Rect(200, 120, 880, 475),
        #         p1=p1,
        #         p2=p2,
        #         canvas=screen
        #     )]
        # ))
        # self.bridge.whileloop(new_view=MovesView(
        #     view=self.bridge.view,
        #     transitions=[DuelSlashTransition(
        #         rect=Rect(200, 120, 880, 475),
        #         p1=p1,
        #         p2=p2,
        #         canvas=screen
        #     )]
        # ))
