from dataclasses import dataclass
from typing import Callable, Protocol, runtime_checkable

from any.locales import kames
# from ctrl.exchange_kards import ExchangeKardsController
# from ctrl.guards import GuardsController
from model.board import Board
from model.player import Player
from ptc.bridge import Bridge
from seed.default_router import router
from view.player_select_view import PlayerSelectView

# @runtime_checkable
# class _PPController(Protocol):
#     def __init__(self, bridge: Bridge) -> None:
#         ...

#     def action(self, p1: Player, p2: Player) -> None:
#         ...

# @runtime_checkable
# class _SController(Protocol):
#     def __init__(self, bridge: Bridge) -> None:
#         ...

#     def action(self, s: str) -> None:
#         ...

@dataclass
class SyougunEffect():
    guards_async: Callable[[str], None]
    exchange_kards_async: Callable[[Player, Player], None]
    # def __init__(
    #         self, guards_controller: type[_SController]=GuardsController,
    #         exchange_kards_controller: type[_PPController]=ExchangeKardsController
    # ) -> None:
    #     '''フックに掛ける非同期処理を担うControllerのクラスのみ注入する。
    #     EffectはBoardの拡張なのでBridgeは実処理時に注入するのみとする。
    #     仮にBridgeを含む何かを注入すると、Bridge.view....Surfaceがdeepcopyできずバグる。

    #     現段階では注入が面倒なので初期化時に直接非同期処理を設定しているが、
    #     いずれはEffect外部で必要に応じてフックに掛ける非同期処理を注入していく。
    #     '''
    #     self.guards_controller = guards_controller
    #     self.exchange_kards_controller = exchange_kards_controller

    def use_func(self, bridge: Bridge, player: Player) -> None:
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
            # exchange_kards_async=self.exchange_kards_controller(bridge=bridge).action,
            # guards_async=self.guards_controller(bridge=bridge).action
        )

    def commit_board(
            self, board: Board, p1: Player, p2: Player,
            # exchange_kards_async: Callable[[Player, Player], None] = lambda p1, p2: None,
            # guards_async: Callable[[str], None] = lambda s: None,
    ) -> None:
        '''Boardのデータを実際に更新する命令。
        非同期処理等のBoard外依存処理を直接は含まない。
        が、guards_asyncやexchage_kards_asyncとしてSyougunEffect作成時に
        注入したContoroller.actionを実行する事で非同期処理を噛ませる事ができる。
        '''
        if p1.protected or p2.protected:
            self.guards_async(kames(folder="syougun", key="name"))
            # guards_async(kames(folder="syougun", key="name"))
            return
        self.exchange_kards_async(p1, p2)
        # exchange_kards_async(p1, p2)
        p1.hands, p2.hands = p2.hands, p1.hands
