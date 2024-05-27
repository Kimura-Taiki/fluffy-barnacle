from typing import NamedTuple

from model.kard import Kard, EMPTY_KARD
from model.deck import make_deck
from model.player import Player, OBSERVER

class Board(NamedTuple):
    players: list[Player]
    deck: list[Kard]
    turn_player: Player=OBSERVER
    draw_kard: Kard=EMPTY_KARD

    @classmethod
    def new_board(cls, players: list[Player]) -> 'Board':
        return Board(players=players, deck=make_deck())