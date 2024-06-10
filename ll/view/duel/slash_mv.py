from pygame import Rect, Vector2 as V2

from any.pictures import IMG_DUEL, IMG_BACK
from model.kard import Kard
from ptc.bridge import Bridge
from ptc.transition import Transition
from view.duel.slash_transition import SlashTransition
from view.transition.static_transition import StaticTransition
from view.moves_view import MovesView

def slash_mv(bridge: Bridge, rect: Rect, k1: Kard, k2: Kard) -> MovesView:
    transitions: list[Transition] = [StaticTransition(
        img_actor=IMG_DUEL,
        center=V2(rect.center),
    )]
    if k1.rank >= k2.rank:
        transitions.append(StaticTransition(
            img_actor=IMG_BACK,
            center=V2(rect.topleft)+V2(170, 240),
        ))
    else:
        transitions.append(SlashTransition(
            img_actor=k1.picture(),
            center=V2(rect.topleft)+V2(170, 240),
        ))
    if k2.rank >= k1.rank:
        transitions.append(StaticTransition(
            img_actor=IMG_BACK,
            center=V2(rect.topright)+V2(-170, 240),
        ))
    else:
        transitions.append(SlashTransition(
            img_actor=k2.picture(),
            center=V2(rect.topright)+V2(-170, 240),
        ))
    return MovesView(view=bridge.view, transitions=transitions)
