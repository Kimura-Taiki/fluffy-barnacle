from typing import Callable, Protocol, runtime_checkable

from any.func import enforce
from any.screen import screen
from ctrl.exchange_kards import ExchangeKardsController
from kard.guard_message import guard_message
from model.board import Board
from model.player import Player
from ptc.bridge import Bridge
from view.board_view import BoardView
from view.transition.linear_transition import LinearTransition
from view.moves_view import MovesView
from view.player_square import PlayerSquare
from view.player_select_view import PlayerSelectView

@runtime_checkable
class _PPController(Protocol):
    def __init__(self, bridge: Bridge) -> None:
        ...

    def action(self, p1: Player, p2: Player) -> None:
        ...

class SyougunEffect():
    def __init__(
            self, guards_async: Callable[[], None]=lambda : print("「将軍」はガードされたよ"),
            exchange_kards_controller: type[_PPController]=ExchangeKardsController
    ) -> None:
        '''カードの効果の段階でBridgeを注入する。
        実際のカード効果を担うEffectにBridgeを置く方が引数の総数が減るし、
        各カードの効果はカード固有のBridgeに限定されるのだから問題無いし、
        Effectは循環参照を回避する為にKardで隔離されているのでEffect.bridgeとした。

        加えて、カード使用中に発動する非同期処理もこの段階で注入する。
        現段階では注入が面倒なので初期化時に直接非同期処理を設定しているが、
        いずれはEffect外部で必要に応じてフックに掛ける非同期処理を注入していく。
        '''
        self.guards_async = guards_async
        self.exchange_kards_controller = exchange_kards_controller

    def use_func(self, bridge: Bridge, player: Player) -> None:
        ...
        # return
        '''カード使用時に呼ばれる命令。
        ２人のプレイヤーを選択するまでを担う。
        プレイヤーがMANかCOMかOBSかで実際の選択が変わり得るが、
        今回はMANである事を見切って実装する。
        COM実装時にはplayer側の関数を用いる形になるだろう。
        選択が完了したら実際のBoard更新処理はcommit_boardに投げる。
        '''
        bridge.whileloop(new_view=(psv := PlayerSelectView(
            bridge=bridge,
            exclude=bridge.board.turn_player,
        )))
        self.commit_board(
            board=bridge.board,
            p1=bridge.board.turn_player,
            p2=psv.selected_player,
            exchange_kards_async=self.exchange_kards_controller(bridge=bridge).action
        )

    def commit_board(
            self, board: Board, p1: Player, p2: Player,
            exchange_kards_async: Callable[[Player, Player], None] = lambda p1, p2: None
    ) -> None:
        '''Boardのデータを実際に更新する命令。
        非同期処理等のBoard外依存処理を直接は含まない。
        が、guards_asyncやexchage_kards_asyncとしてSyougunEffect作成時に
        注入したContoroller.actionを実行する事で非同期処理を噛ませる事ができる。
        '''
        if p1.protected or p2.protected:
            self.guards_async()
            return
        exchange_kards_async(p1, p2)
        p1.hands, p2.hands = p2.hands, p1.hands
        
# def exchange_kards(self, p1: Player, p2: Player) -> None:
#     """二人のプレイヤー間でカードを交換する処理を行います。"""
#     if p1.protected or p2.protected:
#         from model.deck import KARD_SYOUGUN
#         self.guard_async(KARD_SYOUGUN)
#         return
#     self.exchange_kards_async(p1, p2)
#     p1.hands, p2.hands = p2.hands, p1.hands


# def _use_syougun(self) -> None:
#     print("カード「将軍」を使ったよ")
#     self.bridge.whileloop(new_view=(psv := PlayerSelectView(
#         bridge=self.bridge,
#         exclude=self.bridge.board.turn_player,
#     )))
#     self.bridge.board.exchange_kards(
#         p1=self.bridge.board.turn_player,
#         p2=psv.selected_player
#     )
# #       10        20        30        40        50        60        70       79
#     # print(psv.selected_player)
#     # raise EOFError("良し！")

# class ExchangeKardsController():
#     def __init__(self, bridge: Bridge) -> None:
#         self.bridge = bridge
#         self.board_view = enforce(bridge.view, BoardView)
#         self.img_back = self.board_view.deck_square.img_back

#     def action(self, p1: Player, p2: Player) -> None:
#         p1_v2 = PlayerSquare.search_v2_by_player(
#             squares=self.board_view.squares,
#             player=p1,
#         )
#         p2_v2 = PlayerSquare.search_v2_by_player(
#             squares=self.board_view.squares,
#             player=p2
#         )
#         self.bridge.whileloop(new_view=MovesView(
#             view=self.bridge.view,
#             transitions=[
#                 LinearTransition(
#                     img_actor=self.img_back,
#                     from_v2=f,
#                     to_v2=t,
#                     canvas=screen
#                 )
#                 for f, t in [(p1_v2, p2_v2), (p2_v2, p1_v2)]
#             ]
#         ))
