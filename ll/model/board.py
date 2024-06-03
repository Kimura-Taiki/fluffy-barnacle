from dataclasses import dataclass, field
from typing import Callable

from model.kard import Kard
from model.deck import make_deck, KARD_MAZYUTUSI, KARD_SYOUGUN, KARD_HIME, KARD_DAIZIN
from model.player import Player, OBSERVER

@dataclass
class Board:
    players: list[Player]
    deck: list[Kard]
    turn_player: Player = field(default_factory=lambda: OBSERVER)
    draw_kard_async: Callable[[Player], None] = lambda p: None
    turn_start_async: Callable[[], None] = lambda : None
    use_kard_async: Callable[[Player, Kard], None] = lambda p, k: None
    defeat_by_daizin_async: Callable[[Player], None] = lambda p: None
    diskard_hime_async: Callable[[Player], None] = lambda p: None
    protect_async: Callable[[Player], None] = lambda p: None
    guard_async: Callable[[Kard], None] = lambda k: None
    exchange_kards_async: Callable[[Player, Player], None] = lambda p1, p2: None
    rummage_async: Callable[[Player], None] = lambda p: None

    def game_start(self) -> None:
        """ゲームの開始時に呼び出され、最初のターンプレイヤーを設定します。"""
        self.turn_player = self.players[0]

    def draw(self, player: Player) -> None:
        """プレイヤーがカードを引く処理を行います。"""
        self.draw_kard_async(player)
        player.hands.append(self.deck.pop(0))
        if KARD_DAIZIN in player.hands and sum(kard.rank for kard in player.hands) >= 12:
            self.defeat_by_daizin_async(player)
            self.retire(player=player)

    def turn_start(self) -> None:
        self.turn_start_async()
        self.turn_player.protected = False
        self.draw(player=self.turn_player)
        if not self.turn_player.alive:
            self.advance_to_next_turn()
            self.turn_start()

    def use_kard(self, player: Player, kard: Kard) -> None:
        """プレイヤーがカードを使用する処理を行います。"""
        self.use_kard_async(player, kard)
        self.diskard(player=player, kard=kard)

    def diskard(self, player: Player, kard: Kard) -> None:
        """プレイヤーがカードを捨てる処理を行います。"""
        player.hands.remove(kard)
        player.log.append(kard)
        if kard == KARD_HIME:
            self.diskard_hime_async(player)
            self.retire(player=player)

    def retire(self, player: Player) -> None:
        """プレイヤーを退場させる処理を行います。"""
        print(f"{player.name} is out!")
        player.alive = False
        player.log.extend(player.hands)
        player.hands.clear()

    def advance_to_next_turn(self) -> None:
        """次のターンプレイヤーを設定します。"""
        shift = (self.players.index(self.turn_player) + 1) % len(self.players)
        for player in self.players[shift:] + self.players[:shift]:
            if player.alive:
                self.turn_player = player
                return
        raise ValueError("生存者がいません", self)
    
    def protect(self, player: Player) -> None:
        self.protect_async(player)
        player.protected = True

    def rummage(self, player: Player) -> None:
        """プレイヤーがカードを捨てて、新しいカードを引く処理を行います。"""
        if player.protected:
            self.guard_async(KARD_MAZYUTUSI)
            return
        self.diskard(player=player, kard=player.hands[0])
        if player.alive:
            self.rummage_async(player)
            self.draw(player=player)

    def exchange_kards(self, p1: Player, p2: Player) -> None:
        """二人のプレイヤー間でカードを交換する処理を行います。"""
        if p1.protected or p2.protected:
            self.guard_async(KARD_SYOUGUN)
            return
        self.exchange_kards_async(p1, p2)
        p1.hands, p2.hands = p2.hands, p1.hands

    @classmethod
    def new_board(cls, players: list[Player]) -> 'Board':
        """新しいゲームボードを初期化するクラスメソッド。"""
        return Board(players=players, deck=make_deck())
