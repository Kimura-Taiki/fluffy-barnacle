from model.kard import EMPTY_KARD
from model.deck import make_deck
from model.player import Player, OBSERVER

class Board():
    def __init__(self, players: list[Player]) -> None:
        self.players = players
        self.deck = make_deck()
        self.players = [player._replace(hand=self.deck.pop(0), alive=True) for player in self.players]
        self.turn_player = OBSERVER
        self.draw_kard = EMPTY_KARD
