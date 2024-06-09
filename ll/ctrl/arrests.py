from pygame import Rect, Vector2 as V2, Surface, SRCALPHA, transform

from any.pictures import IMG_WANTED, IMG_BACK, IMG_DUEL
from any.screen import screen
from model.kard import Kard
from model.player import Player
from ptc.bridge import Bridge
from view.linear_transition import LinearTransition
from view.transition.zoom_transition import ZoomTransitions
# from view.arrest.engage_transition import EngageTransition
# from view.arrest.open_transition import OpenTransition
# from view.arrest.slash_transition import SlashTransition
from view.moves_view import MovesView

def _img_wanted(kard: Kard) -> Surface:
    img = Surface(size=IMG_WANTED.get_size(), flags=SRCALPHA)
    img.blit(
        source=transform.rotozoom(
            surface=kard.picture(),
            angle=0.0,
            scale=1.5
        ),
        dest=(20, 160),
        area=Rect(105, 240, 300, 300)
    )
    img.blit(source=IMG_WANTED, dest=(0, 0))
    return img

_Rect = Rect(200, 120, 880, 480)
_Huda = V2(340, 475)

class ArrestsController():
    def __init__(self, bridge: Bridge) -> None:
        self.bridge = bridge

    def action(self, player: Player, kard: Kard) -> None:
        self.bridge.whileloop(new_view=MovesView(
            view=self.bridge.view,
            transitions=[ZoomTransitions(
                img_actor=IMG_DUEL,
                center=V2(_Rect.center),
                from_scale=3.0,
                to_scale=1.0,
                canvas=screen
            ),
            LinearTransition(
                img_actor=_img_wanted(kard=kard),
                from_v2=V2(
                    200+170-340*2,
                    120+240
                ),
                to_v2=V2(200+170, 120+240),
                canvas=screen
            ),
            LinearTransition(
                img_actor=IMG_BACK,
                from_v2=V2(1080-170+340*2, 120+240),
                to_v2=V2(1080-170, 120+240),
                canvas=screen
            )]
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
