#       10        20        30        40        50        60        70       79
from dataclasses import dataclass, field
from typing import Callable

from model.kard import Kard
# from model.deck import make_deck, KARD_HEISI, KARD_DOUKE, KARD_KISI,\
#     KARD_MAZYUTUSI, KARD_SYOUGUN, KARD_HIME, KARD_DAIZIN
from model.player import Player, OBSERVER

@dataclass
class Board:
    players: list[Player]
    deck: list[Kard]
    turn_player: Player = field(default_factory=lambda: OBSERVER)
    reserve: list[Kard] = field(default_factory=lambda: [])

    draw_kard_async: Callable[[Player], None] = lambda p: None
    turn_start_async: Callable[[], None] = lambda : None
    use_kard_async: Callable[[Player, Kard], None] = lambda p, k: None
    win_by_survival_async: Callable[[Player], None] = lambda p: None
    win_by_strength_async: Callable[[Player], None] = lambda p: None

    # arrest_async: Callable[[Player, Kard], None] = lambda p, k: None
    # peep_async: Callable[[Player, Player, Player], None] = lambda p1, p2, p3: None
    # duel_async: Callable[[Player, Player], None] = lambda p1, p2: None
    # defeat_by_duel_async: Callable[[Player], None] = lambda p: None
    # protect_async: Callable[[Player], None] = lambda p: None
    # guard_async: Callable[[Kard], None] = lambda k: None
    # exchange_kards_async: Callable[[Player, Player], None] = lambda p1, p2: None
    # rummage_async: Callable[[Player], None] = lambda p: None
    # defeat_by_daizin_async: Callable[[Player], None] = lambda p: None
    # diskard_hime_async: Callable[[Player], None] = lambda p: None

    def game_start(self) -> None:
        """ゲームの開始時に呼び出され、最初のターンプレイヤーを設定します。"""
        self.reserve.append(self.deck.pop(-1))
        self.turn_player = self.players[0]

    def draw(self, player: Player) -> None:
        """プレイヤーがカードを引く処理を行います。"""
        self.draw_kard_async(player)
        player.hands.append(self.deck.pop(0))
        # from model.deck import KARD_DAIZIN
        # if KARD_DAIZIN in player.hands and sum(kard.rank for kard in player.hands) >= 12:
        #     self.defeat_by_daizin_async(player)
        #     self.retire(player=player)

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
        kard.use_func(self, self.turn_player)

    def diskard(self, player: Player, kard: Kard) -> None:
        """プレイヤーがカードを捨てる処理を行います。"""
        player.hands.remove(kard)
        player.log.append(kard)
        # from model.deck import KARD_HIME
        # if kard == KARD_HIME:
        #     self.diskard_hime_async(player)
        #     self.retire(player=player)

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
    
    # def arrest(self, player: Player, kard: Kard) -> None:
    #     if player.protected:
    #         from model.deck import KARD_HEISI
    #         self.guard_async(KARD_HEISI)
    #         return
    #     self.arrest_async(player, kard)
    #     if player.hands[0] == kard:
    #         self.retire(player=player)

    # def peep(self, peeper: Player, watched: Player, subject: Player) -> None:
    #     if watched.protected:
    #         from model.deck import KARD_DOUKE
    #         self.guard_async(KARD_DOUKE)
    #         return
    #     self.peep_async(peeper, watched, subject)

    # def duel(self, p1: Player, p2: Player) -> None:
    #     if p1.protected or p2.protected:
    #         from model.deck import KARD_KISI
    #         self.guard_async(KARD_KISI)
    #         return
    #     self.duel_async(p1, p2)
    #     if p1.hands[0].rank > p2.hands[0].rank:
    #         self.defeat_by_duel_async(p2)
    #         self.retire(player=p2)
    #     elif p1.hands[0].rank < p2.hands[0].rank:
    #         self.defeat_by_duel_async(p1)
    #         self.retire(player=p1)

    # def protect(self, player: Player) -> None:
    #     self.protect_async(player)
    #     player.protected = True

    # def rummage(self, player: Player) -> None:
    #     """プレイヤーがカードを捨てて、新しいカードを引く処理を行います。"""
    #     if player.protected:
    #         from model.deck import KARD_MAZYUTUSI
    #         self.guard_async(KARD_MAZYUTUSI)
    #         return
    #     self.diskard(player=player, kard=player.hands[0])
    #     if player.alive:
    #         self.rummage_async(player)
    #         self.draw(player=player)

    # def exchange_kards(self, p1: Player, p2: Player) -> None:
    #     """二人のプレイヤー間でカードを交換する処理を行います。"""
    #     if p1.protected or p2.protected:
    #         from model.deck import KARD_SYOUGUN
    #         self.guard_async(KARD_SYOUGUN)
    #         return
    #     self.exchange_kards_async(p1, p2)
    #     p1.hands, p2.hands = p2.hands, p1.hands

    @classmethod
    def new_board(cls, players: list[Player]) -> 'Board':
        """新しいゲームボードを初期化するクラスメソッド。"""
        from model.deck import make_deck
        return Board(players=players, deck=make_deck())
        # board = Board(players=players, deck=make_deck())
        # for kard in board.deck:
        #     verb = kard.use_func
        #     # verb(board)
        #     # kard.use_func(board, )
        #     print("heei", kard, verb)
        # return board