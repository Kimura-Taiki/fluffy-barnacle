from dataclasses import dataclass
from typing import Callable

from any.func import enforce
from any.locales import kames
from model.board import Board
from model.player import Player
from ptc.bridge import Bridge
# from ptc.main_view import MainView
from view.board_view import BoardView
from view.player_select_view import PlayerSelectView

@dataclass
class DoukeEffect():
    guards_async: Callable[[str], None]
    peeps_async: Callable[[Player, Player, Player], None]
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
            peeper=player,
            watched=psv.selected_player,
            subject=enforce(bridge.view, BoardView).subject
        )

    def commit_board(
            self, board: Board, peeper: Player, watched: Player, subject: Player,
    ) -> None:
        '''Boardのデータを実際に更新する命令。
        非同期処理等のBoard外依存処理を直接は含まない。
        が、guards_asyncやexchage_kards_asyncとしてSyougunEffect作成時に
        注入したContoroller.actionを実行する事で非同期処理を噛ませる事ができる。
        '''
        if watched.protected:
            self.guards_async(kames(folder="douke", key="name"))
            return
        self.peeps_async(peeper, watched, subject)
