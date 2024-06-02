from any.pictures import IMG_BACK
from model.kard import Kard
from model.player import Player
from ptc.bridge import Bridge
from view.linear_transition import LinearTransition
from view.moves_view import MovesView
from view.use_kard_view import UseKardView

class ExchangeKardsController():
    def __init__(self, bridge: Bridge) -> None:
        self.bridge = bridge

    def action(self, p1: Player, p2: Player) -> None:
        self.bridge.whileloop(new_view=MovesView(
            view=self.bridge.view,
            transitions=[
                LinearTransition(
                    img_actor=IMG_BACK,
                    
                )
            ]
        ))

    # def action(self, player: Player, kard: Kard) -> None:
    #     self.bridge.whileloop(new_view=UseKardView(
    #         view=self.bridge.view,
    #         kard=kard,
    #     ))
