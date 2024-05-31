from any.font import MS_MINCHO_COL
from ctrl.draw_kards import DrawKardsController
from ctrl.messages import MessagesController
from ctrl.turn_starts import TurnStartsController
from model.kard import Kard
from ptc.bridge import Bridge
from view.board_view import BoardView
from view.message_view import MessageView
from view.use_kard_view import UseKardView

_FONT = 28

from ptc.controller import Controller
class UseKardsController():
    def __init__(self, bridge: Bridge, kard: Kard) -> None:
        # print("UseKardsController.__init__")
        self.bridge = bridge
        self.kard = kard

    def action(self) -> None:
        # print("UseKardsController.action")
        self.bridge.board.use_kard(player=self.bridge.board.turn_player, kard=self.kard)
        self._old_view = self.bridge.view
        self.bridge.view = UseKardView(
            view=self._old_view,
            kard=self.kard,
            callback=self._callback
        )

    def _callback(self) -> None:
        self.bridge.view = self._old_view
        # print("UseKardsController._callback", self.bridge.view)
        coroutines = [
            self._use_banpei, self._use_heisi, self._use_douke, self._use_kisi, self._use_souryo,
            self._use_mazyutusi, self._use_syougun, self._use_daizin, self._use_hime
        ]
        coroutines[self.kard.rank]()
        # self.bridge.board.advance_to_next_turn()
        # TurnStartsController(bridge=self.bridge).action()

    def _advance_to_next_turn(self) -> None:
        self.bridge.board.advance_to_next_turn()
        TurnStartsController(bridge=self.bridge).action()

    def _use_banpei(self) -> None:
        raise ValueError("番兵は使う想定にありません")

    def _use_heisi(self) -> None:
        print("カード「兵士」を使ったよ")
        self._advance_to_next_turn()

    def _use_douke(self) -> None:
        print("カード「道化」を使ったよ")
        self._advance_to_next_turn()

    def _use_kisi(self) -> None:
        print("カード「騎士」を使ったよ")
        self._advance_to_next_turn()

    def _use_souryo(self) -> None:
        print("カード「僧侶」を使ったよ")
        self._advance_to_next_turn()

    def _use_mazyutusi(self) -> None:
        print("カード「魔術師」を使ったよ")
        self._advance_to_next_turn()

    def _use_syougun(self) -> None:
        print("カード「将軍」を使ったよ")
        self._advance_to_next_turn()

    def _use_daizin(self) -> None:
        print("カード「大臣」を使ったよ")
        self._advance_to_next_turn()

    def _use_hime(self) -> None:
        print("UseKardsController._use_hime", self.bridge.view)
        MessagesController(
            bridge=self.bridge,
            img_mes=MS_MINCHO_COL(f"「姫」を捨てたので{self.bridge.board.turn_player.name}は脱落します", _FONT, "black"),
            suffix=self._advance_to_next_turn
            # suffix=self._suffix
        ).action()

    # def _suffix(self) -> None:
    #     print("UseKardsController._suffix", self.bridge.view)
    #     print("カード「姫」を使ったよ")

    # def action(self) -> None:
    #     handless_player = next((
    #         player for player in self.bridge.board.players if len(player.hands) == 0
    #     ), None)
    #     view = self.bridge.view
    #     if not isinstance(view, BoardView):
    #         raise ValueError("SetupsControllerを起動する時はBoardViewでないと")
    #     if handless_player:
    #         DrawKardsController(
    #             bridge=self.bridge,
    #             board_view=view,
    #             player=handless_player,
    #             suffix=self._draw_suffix
    #         ).action()
    #     else:
    #         self._game_start()

    # def _draw_suffix(self) -> None:
    #     self.action()

    # def _game_start(self) -> None:
    #     self.bridge.board.game_start()
    #     TurnStartsController(bridge=self.bridge).action()
