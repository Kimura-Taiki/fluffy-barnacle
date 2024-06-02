from model.kard import Kard
from model.player import Player
from ptc.bridge import Bridge
from view.use_kard_view import UseKardView

class BrightKardsController():
    def __init__(self, bridge: Bridge) -> None:
        self.bridge = bridge

    def action(self, player: Player, kard: Kard) -> None:
        self.bridge.whileloop(new_view=UseKardView(
            view=self.bridge.view,
            kard=kard,
        ))
