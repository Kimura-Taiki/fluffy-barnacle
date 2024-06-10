from pygame import Rect, Vector2 as V2, Surface

from any.pictures import IMG_ARREST
from any.screen import screen
from model.kard import Kard
from ptc.bridge import Bridge
from view.arrest.img_wanted import img_wanted
from view.transition.face_up_transition import FaceUpTransition
from view.transition.static_transition import StaticTransition
from view.moves_view import MovesView

def face_up_mv(bridge: Bridge, rect: Rect, kard: Kard, img_after: Surface) -> MovesView:
    return MovesView(
        view=bridge.view,
        transitions=[StaticTransition(
            img_actor=IMG_ARREST,
            center=V2(rect.center),
            canvas=screen
        ),
        StaticTransition(
            img_actor=img_wanted(kard=kard),
            center=V2(rect.topleft)+V2(170, 240),
            canvas=screen
        ),
        FaceUpTransition(
            img_after=img_after,
            center=V2(rect.topright)+V2(-170, 240),
            canvas=screen
        )]
    )
