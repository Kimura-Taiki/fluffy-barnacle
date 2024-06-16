#       10        20        30        40        50        60        70       79
from dataclasses import dataclass, field
from typing import Callable

from model.kard import Kard
from model.player import Player, OBSERVER

@dataclass
class Board:
    players: list[Player] = field(default_factory=lambda : [])
    deck: list[Kard] = field(default_factory=lambda : [])
    turn_player: Player = field(default_factory=lambda : OBSERVER)
    reserve: list[Kard] = field(default_factory=lambda : [])

    draw_kard_async: Callable[[Player], None] = lambda p: None
    drawn_func_async: Callable[[Player, Kard], None] = lambda p, k: None
    turn_start_async: Callable[[], None] = lambda : None
    use_kard_async: Callable[[Player, Kard], None] = lambda p, k: None
    diskard_func_async: Callable[[Player, Kard], None] = lambda p, k: None
    win_by_survival_async: Callable[[Player], None] = lambda p: None
    win_by_strength_async: Callable[[Player], None] = lambda p: None

    def game_start(self) -> None:
        """ゲームの開始時に呼び出され、最初のターンプレイヤーを設定します。"""
        self.reserve.append(self.deck.pop(-1))
        self.turn_player = self.players[0]

    def draw(self, player: Player) -> None:
        """プレイヤーがカードを引く処理を行います。"""
        self.draw_kard_async(player)
        player.hands.append(kard := self.deck.pop(0))
        self.drawn_func_async(player, kard)

    def turn_start(self) -> None:
        if len(self.deck) == 0:
            for winner in self.highest_ranked_alive_players():
                self.win_by_strength_async(winner)
            exit()
        self.turn_start_async()
        self.turn_player.protected = False
        self.draw(player=self.turn_player)
        if not self.turn_player.alive:
            self.advance_to_next_turn()
            self.turn_start()

    def highest_ranked_alive_players(self) -> list[Player]:
        alive_players = [player for player in self.players if player.alive]
        max_rank = max(player.hands[0].rank for player in alive_players)
        return [player for player in alive_players if player.hands[0].rank == max_rank]

    def use_kard(self, player: Player, kard: Kard) -> None:
        """プレイヤーがカードを使用する処理を行います。"""
        self.use_kard_async(player, kard)
        self.diskard(player=player, kard=kard)

    def diskard(self, player: Player, kard: Kard) -> None:
        """プレイヤーがカードを捨てる処理を行います。"""
        player.hands.remove(kard)
        player.log.append(kard)
        self.diskard_func_async(player, kard)

    def retire(self, player: Player) -> None:
        """プレイヤーを退場させる処理を行います。"""
        print(f"{player.name} is out!")
        player.alive = False
        player.log.extend(player.hands)
        player.hands.clear()
        if len((winner := [player for player in self.players if player.alive])) == 1:
            self.win_by_survival_async(winner[0])
            exit()

    def advance_to_next_turn(self) -> None:
        """次のターンプレイヤーを設定します。"""
        shift = (self.players.index(self.turn_player) + 1) % len(self.players)
        for player in self.players[shift:] + self.players[:shift]:
            if player.alive:
                self.turn_player = player
                return
        raise ValueError("生存者がいません", self)
    