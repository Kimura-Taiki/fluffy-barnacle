from dataclasses import dataclass, field
from typing import Callable

from model.kard import Kard
from model.deck import make_deck, KARD_HIME, KARD_DAIZIN
from model.player import Player, OBSERVER

@dataclass
class Board():
    players: list[Player]
    deck: list[Kard]
    turn_player: Player = field(default_factory=lambda: OBSERVER)
    use_kard_async: Callable[[Player, Kard], None] = lambda p, k : None
    defeat_by_daizin_async: Callable[[Player], None] = lambda p : None
    diskard_hime_async: Callable[[Player], None] = lambda p : None

    def game_start(self) -> None:
        self.turn_player = self.players[0]

    def draw(self, player: Player) -> None:
        player.hands.append(self.deck.pop(0))
        if KARD_DAIZIN in player.hands and sum([kard.rank for kard in player.hands]) >= 12:
            self.defeat_by_daizin_async(player)
            self.retire(player=player)

    def use_kard(self, player: Player, kard: Kard) -> None:
        self.use_kard_async(player, kard)
        self.diskard(player=player, kard=kard)

    def diskard(self, player: Player, kard: Kard) -> None:
        player.hands.remove(kard)
        player.log.append(kard)
        if kard == KARD_HIME:
            self.diskard_hime_async(player)
            self.retire(player=player)

    def retire(self, player: Player) -> None:
        print(f"{player.name} is out!")
        player.alive = False
        while len(player.hands) > 0:
            kard = player.hands[0]
            player.hands.remove(kard)
            player.log.append(kard)

    def advance_to_next_turn(self) -> None:
        shift = (self.players.index(self.turn_player)+1)%len(self.players)
        for player in self.players[shift:]+self.players[:shift]:
            if player.alive:
                self.turn_player = player
                return
        raise ValueError("生存者がいません", self)

    def exchange_kards(self, p1: Player, p2: Player) -> None:
        hands1, hands2 = p1.hands, p2.hands
        p1.hands, p2.hands = hands2, hands1

    @classmethod
    def new_board(cls, players: list[Player]) -> 'Board':
        return Board(players=players, deck=make_deck())