from typing import NamedTuple

from model.kard import Kard, EMPTY_KARD
from model.deck import make_deck
from model.player import Player, OBSERVER
# from ptc.bridge import Bridge

class Board(NamedTuple):
    players: list[Player]
    deck: list[Kard]
    turn_player: Player=OBSERVER
    draw_kard: Kard=EMPTY_KARD

    def use_draw_kard(self) -> None:
        idx = self.turn_player_index
        self.use_kard(
            idx=idx,
            use=self.draw_kard,
            rest=self.players[idx].hand
        )

    def use_hand_kard(self) -> None:
        idx = self.turn_player_index
        self.use_kard(
            idx=idx,
            use=self.players[idx].hand,
            rest=self.draw_kard
        )

    # def hoge(self, bridge: Bridge) -> None:
    #     ...

    def use_kard(self, idx: int, use: Kard, rest: Kard) -> None:
        self.players[idx] = self.players[idx]._replace(
            hand=rest,
            log=self.players[idx].log+[use]
        )
        self = self._replace(
            draw_kard=EMPTY_KARD
        )
        print(f"Use {use}", f"Board ID : {id(self)}")

    def advance_to_next_turn(self) -> None:
        shift = (self.turn_player_index+1)%len(self.players)
        for player in self.players[shift:]+self.players[:shift]:
            if player.alive:
                self = self._replace(
                    turn_player=player
                )
                return
        raise ValueError("生存者がいません", self)

    def named_player(self, name: str) -> Player:
        return self.players[self.name_index(name)]

    def name_index(self, name: str) -> int:
        return [player.name for player in self.players].index(name)

    @property
    def turn_player_index(self) -> int:
        return self.name_index(self.turn_player.name)

    @classmethod
    def new_board(cls, players: list[Player]) -> 'Board':
        return Board(players=players, deck=make_deck())