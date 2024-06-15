from pygame import Rect, Vector2 as V2

from any.locales import kames
from any.pictures import IMG_DUEL, IMG_BACK
from model.player import Player
from ptc.bridge import Bridge
from ptc.transition import Transition
from view.transition.message_transition import MessageTransition
from view.transition.static_transition import StaticTransition
from view.moves_view import MovesView

def result_mv(bridge: Bridge, rect: Rect, p1: Player, p2:Player) -> MovesView:
    loser = p1 if p1.hand.rank < p2.hand.rank else p2
    transitions: list[Transition] = [StaticTransition(
        img_actor=IMG_DUEL,
        center=V2(rect.center),
    )]
    if loser == p2:
        transitions.append(StaticTransition(
            img_actor=IMG_BACK,
            center=V2(rect.topleft)+V2(170, 240),
        ))
    if loser == p1:
        transitions.append(StaticTransition(
            img_actor=IMG_BACK,
            center=V2(rect.topright)+V2(-170, 240),
        ))
    transitions.append(MessageTransition(
        img_mes=kames(folder="kisi", key="defeat_by_duels", player_name=loser.name),
    ))
    return MovesView(view=bridge.view, transitions=transitions)
