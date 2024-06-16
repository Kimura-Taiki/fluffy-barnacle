from model.kard import Kard
from model.player import Player
from ptc.bridge import Bridge

from ptc.controller import Controller
class DiscardFuncsController():
    def __init__(self, bridge: Bridge,) -> None:
        self.bridge = bridge

    def action(self, player: Player, kard: Kard) -> None:
        kard.discard_func(bridge=self.bridge, player=player)
