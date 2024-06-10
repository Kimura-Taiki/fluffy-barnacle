from pygame import Rect, Vector2 as V2

from any.pictures import IMG_ARREST, IMG_HAZURE
from model.kard import Kard
from ptc.bridge import Bridge
from view.arrest.img_wanted import img_wanted
from view.transition.static_transition import StaticTransition
from view.moves_view import MovesView

def hazure_mv(bridge: Bridge, rect: Rect, kard: Kard) -> MovesView:
    return MovesView(
        view=bridge.view,
        transitions=[StaticTransition(
            img_actor=IMG_ARREST,
            center=V2(rect.center),
        ),
        StaticTransition(
            img_actor=img_wanted(kard=kard),
            center=V2(rect.topleft)+V2(170, 240),
        ),
        StaticTransition(
            img_actor=IMG_HAZURE,
            center=V2(rect.topright)+V2(-170, 240),
        )]
    )
