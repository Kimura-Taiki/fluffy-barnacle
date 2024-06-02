from ctrl.turn_starts import TurnStartsController
from model.kard import Kard
from ptc.bridge import Bridge
from view.player_select_view import PlayerSelectView

from ptc.controller import Controller
class UseKardsController():
    def __init__(self, bridge: Bridge, kard: Kard) -> None:
        self.bridge = bridge
        self.kard = kard

    def action(self) -> None:
        self.bridge.board.use_kard(player=self.bridge.board.turn_player, kard=self.kard)
        coroutines = [
            self._use_banpei, self._use_heisi, self._use_douke, self._use_kisi, self._use_souryo,
            self._use_mazyutusi, self._use_syougun, self._use_daizin, self._use_hime
        ]
        coroutines[self.kard.rank]()
        self.bridge.board.advance_to_next_turn()
        TurnStartsController(bridge=self.bridge).action()

    def _use_banpei(self) -> None:
        raise ValueError("番兵は使う想定にありません")

    def _use_heisi(self) -> None:
        print("カード「兵士」を使ったよ")

    def _use_douke(self) -> None:
        print("カード「道化」を使ったよ")

    def _use_kisi(self) -> None:
        print("カード「騎士」を使ったよ")

    def _use_souryo(self) -> None:
        print("カード「僧侶」を使ったよ")

    def _use_mazyutusi(self) -> None:
        print("カード「魔術師」を使ったよ")

    def _use_syougun(self) -> None:
        print("カード「将軍」を使ったよ")
        self.bridge.whileloop(new_view=PlayerSelectView(
            bridge=self.bridge,
            exclude=self.bridge.board.turn_player,
        ))

    def _use_daizin(self) -> None:
        print("カード「大臣」を使ったよ")

    def _use_hime(self) -> None:
        ...
