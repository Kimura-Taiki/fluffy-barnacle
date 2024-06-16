from dataclasses import dataclass
from typing import Callable

from any.locales import kames
from model.board import Board
from model.effect import Effect
from model.kard import Kard
from model.kard_id import KardID
from model.player import Player
from ptc.bridge import Bridge
from view.kard_select_view import KardSelectView
from view.player_select_view import PlayerSelectView

@dataclass
class HeisiEffect():
    guards_async: Callable[[str], None]
    arrests_async: Callable[[Player, Kard], None]
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
        bridge.whileloop(new_view=(ksv := KardSelectView(
            bridge=bridge,
            select_list=_board_rest_kards(board=bridge.board)
        )))
        self.commit_board(
            board=bridge.board,
            player=psv.selected_player,
            kard=ksv.selected_kard,
        )

    def commit_board(
            self, board: Board, player: Player, kard: Kard
    ) -> None:
        '''Boardのデータを実際に更新する命令。
        非同期処理等のBoard外依存処理を直接は含まない。
        が、guards_asyncやexchage_kards_asyncとしてSyougunEffect作成時に
        注入したContoroller.actionを実行する事で非同期処理を噛ませる事ができる。
        '''
        if player.protected:
            self.guards_async(kames(folder="heisi", key="name"))
            return
        self.arrests_async(player, kard)
        if player.hand == kard:
            board.retire(player=player)

    @property
    def effect(self) -> Effect:
        return Effect(use_func=self.use_func)

def _board_rest_kards(board: Board) -> list[Kard]:
    all_kards: list[Kard] = []
    all_kards.extend(board.reserve)
    all_kards.extend(board.deck)
    for player in board.players:
        all_kards.extend(player.hands)
    li: list[Kard] = []
    for kard in all_kards:
        if kard not in li:
            li.append(kard)
    brk = sorted(list(li), key=lambda kard: kard.rank)
    print(brk[0].id, KardID.HEISI)
    if brk[0].id == KardID.HEISI:
        brk.pop(0)
    return brk