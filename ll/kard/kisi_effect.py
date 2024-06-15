from dataclasses import dataclass
from typing import Callable

from any.locales import kames
from model.board import Board
from model.player import Player
from ptc.bridge import Bridge
from view.player_select_view import PlayerSelectView

@dataclass
class KisiEffect():
    guards_async: Callable[[str], None]
    duels_async: Callable[[Player, Player], None]
    '''フックに掛ける非同期処理を担うController.action命令を注入する。
    '''

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
        )

    def commit_board(
            self, board: Board, p1: Player, p2: Player,
    ) -> None:
        '''Boardのデータを実際に更新する命令。
        非同期処理等のBoard外依存処理を直接は含まない。
        が、guards_asyncやexchage_kards_asyncとしてSyougunEffect作成時に
        注入したContoroller.actionを実行する事で非同期処理を噛ませる事ができる。
        '''
        if p1.protected or p2.protected:
            self.guards_async(kames(folder="kisi", key="name"))
            return
        self.duels_async(p1, p2)
        if p1.hand.rank > p2.hand.rank:
            board.retire(player=p2)
        elif p2.hand.rank > p1.hand.rank:
            board.retire(player=p1)