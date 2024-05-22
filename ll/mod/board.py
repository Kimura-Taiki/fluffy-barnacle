from mod.deck import make_deck
from ptc.player import Player

class Board():
    def __init__(self, players: list[Player]) -> None:
        self.players = players
        self.deck = make_deck()
        for player in self.players:
            player.hand = self.deck.pop(0)
