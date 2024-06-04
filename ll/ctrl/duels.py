from pygame import Rect

from any.screen import screen
from model.player import Player
from ptc.bridge import Bridge
from view.duel_engage_transition import DuelEngageTransition
from view.duel_open_transition import DuelOpenTransition
from view.duel_slash_transition import DuelSlashTransition
from view.moves_view import MovesView

class DuelsController():
    def __init__(self, bridge: Bridge) -> None:
        self.bridge = bridge

    def action(self, p1: Player, p2: Player) -> None:
        self.bridge.whileloop(new_view=MovesView(
            view=self.bridge.view,
            transitions=[DuelEngageTransition(
                rect=Rect(200, 120, 880, 475),
                p1=p1,
                p2=p2,
                canvas=screen
            )]
        ))
        self.bridge.whileloop(new_view=MovesView(
            view=self.bridge.view,
            transitions=[DuelOpenTransition(
                rect=Rect(200, 120, 880, 475),
                p1=p1,
                p2=p2,
                canvas=screen
            )]
        ))
        self.bridge.whileloop(new_view=MovesView(
            view=self.bridge.view,
            transitions=[DuelSlashTransition(
                rect=Rect(200, 120, 880, 475),
                p1=p1,
                p2=p2,
                canvas=screen
            )]
        ))
