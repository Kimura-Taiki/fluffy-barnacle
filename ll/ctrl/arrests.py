from pygame import Rect, Vector2 as V2

from any.pictures import IMG_WANTED
from any.screen import screen
from model.kard import Kard
from model.player import Player
from ptc.bridge import Bridge
from view.linear_transition import LinearTransition
# from view.arrest.engage_transition import EngageTransition
# from view.arrest.open_transition import OpenTransition
# from view.arrest.slash_transition import SlashTransition
from view.moves_view import MovesView

class ArrestsController():
    def __init__(self, bridge: Bridge) -> None:
        self.bridge = bridge

    def action(self, player: Player, kard: Kard) -> None:
        self.bridge.whileloop(new_view=MovesView(
            view=self.bridge.view,
            # transitions=[EngageTransition(
            #     rect=Rect(200, 120, 880, 475),
            #     p1=p1,
            #     p2=p2,
            #     canvas=screen
            # ),
            # LinearTransition(
            transitions=[LinearTransition(
                img_actor=IMG_WANTED,
                from_v2=V2(200+170-340*2, 120+240),
                to_v2=V2(200+170, 120+240),
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
