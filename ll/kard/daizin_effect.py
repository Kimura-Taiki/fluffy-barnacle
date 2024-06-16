from dataclasses import dataclass
from typing import Callable

from model.board import Board
from model.effect import Effect
from model.player import Player
from ptc.bridge import Bridge

@dataclass
class DaizinEffect():
    defeat_by_ministers: Callable[[Player], None]
    '''フックに掛ける非同期処理を担うController.action命令を注入する。
    '''

    def drawn_func(self, bridge: Bridge, player: Player) -> None:
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
        if sum(kard.rank for kard in player.hands) >= 12:
            self.defeat_by_ministers(player)
            board.retire(player=player)
            return

    @property
    def effect(self) -> Effect:
        return Effect(drawn_func=self.drawn_func)
