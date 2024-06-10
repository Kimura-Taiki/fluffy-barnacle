from pygame import Rect, Vector2 as V2

from any.pictures import IMG_BACK, IMG_DUEL
from ptc.bridge import Bridge
from view.transition.linear_transition import LinearTransition
from view.transition.zoom_transition import ZoomTransition
from view.moves_view import MovesView

def engage_mv(bridge: Bridge, rect: Rect) -> MovesView:
    return MovesView(
        view=bridge.view,
        transitions=[ZoomTransition(
            img_actor=IMG_DUEL,
            center=V2(rect.center),
            from_scale=3.0,
            to_scale=1.0,
        ),
        LinearTransition(
            img_actor=IMG_BACK,
            from_v2=V2(
                200+170-340*2,
                120+240
            ),
            to_v2=V2(200+170, 120+240),
        ),
        LinearTransition(
            img_actor=IMG_BACK,
            from_v2=V2(1080-170+340*2, 120+240),
            to_v2=V2(1080-170, 120+240),
        )]
    )
