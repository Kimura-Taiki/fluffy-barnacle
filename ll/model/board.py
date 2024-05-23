from model.kard import EMPTY_KARD
from model.deck import make_deck
from ptc.player import Player, OBSERVER

class Board():
    def __init__(self, players: list[Player]) -> None:
        self.players = players
        self.deck = make_deck()
        for player in self.players:
            player.hand = self.deck.pop(0)
            player.alive = True
        self.turn_player = OBSERVER
        self.draw_kard = EMPTY_KARD
