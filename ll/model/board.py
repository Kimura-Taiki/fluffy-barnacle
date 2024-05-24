from typing import NamedTuple

from model.kard import Kard, EMPTY_KARD
from model.deck import make_deck
from model.player import Player, OBSERVER

# class Board():
#     def __init__(self, players: list[Player]) -> None:
#         self.players = players
#         self.deck = make_deck()
#         self.players = [player._replace(hand=self.deck.pop(0), alive=True) for player in self.players]
#         self.turn_player = OBSERVER
#         self.draw_kard = EMPTY_KARD

class Board(NamedTuple):
    players: list[Player]
    deck: list[Kard]
    turn_player: Player=OBSERVER
    draw_kard: Kard=EMPTY_KARD

    @classmethod
    def new_board(cls, players: list[Player]) -> 'Board':
        deck = make_deck()
        pls = [player._replace(hand=deck.pop(0), alive=True) for player in players]
        return Board(
            players=pls,
            deck=deck,
        )