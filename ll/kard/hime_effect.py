from dataclasses import dataclass
from typing import Callable

from model.board import Board
from model.effect import Effect
from model.player import Player
from ptc.bridge import Bridge

@dataclass
class HimeEffect():
    diskard_himes_async: Callable[[Player], None]
    '''フックに掛ける非同期処理を担うController.action命令を注入する。
    '''

    def diskard_func(self, bridge: Bridge, player: Player) -> None:
        '''ドロー時に呼ばれる命令。
        '''
        self.commit_board(
            board=bridge.board,
            player=player,
        )

    def commit_board(
            self, board: Board, player: Player,
    ) -> None:
        '''Boardのデータを実際に更新する命令。
        '''
        self.diskard_himes_async(player)
        board.retire(player=player)

    @property
    def effect(self) -> Effect:
        return Effect(diskard_func=self.diskard_func)
