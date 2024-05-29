from dataclasses import dataclass, field

from model.kard import Kard
from model.deck import make_deck
from model.player import Player, OBSERVER

@dataclass
class Board():
    players: list[Player]
    deck: list[Kard]
    turn_player: Player = field(default_factory=lambda: OBSERVER)


    def game_start(self) -> None:
        self.turn_player = self.players[0]

    def draw(self, player: Player) -> None:
        player.hands.append(self.deck.pop(0))

    def use_kard(self, player: Player, kard: Kard) -> None:
        self.diskard(player=player, kard=kard)
        print(f"Use kard {kard}")
        print(player.hands)

    def diskard(self, player: Player, kard: Kard) -> None:
        player.hands.remove(kard)
        player.log.append(kard)

    def advance_to_next_turn(self) -> None:
        shift = (self.players.index(self.turn_player)+1)%len(self.players)
        for player in self.players[shift:]+self.players[:shift]:
            if player.alive:
                self.turn_player = player
                return
        raise ValueError("生存者がいません", self)

    @classmethod
    def new_board(cls, players: list[Player]) -> 'Board':
        return Board(players=players, deck=make_deck())