from dataclasses import dataclass
from typing import Callable

from any.locales import kames
from model.board import Board
from model.player import Player
from ptc.bridge import Bridge
from view.player_select_view import PlayerSelectView

@dataclass
class WizardEffect():
    guards_async: Callable[[str], None]
    '''フックに掛ける非同期処理を担うController.action命令を注入する。
    '''

    def use_func(self, bridge: Bridge, player: Player) -> None:
        '''カード使用時に呼ばれる命令。
        '''
        bridge.whileloop(new_view=(psv := PlayerSelectView(
            bridge=bridge,
        )))
        self.commit_board(
            board=bridge.board,
            player=psv.selected_player,
        )

    def commit_board(
            self, board: Board, player: Player,
    ) -> None:
        '''Boardのデータを実際に更新する命令。
        '''
        if player.protected:
            self.guards_async(kames(folder="mazyutusi", key="name"))
            return
        board.diskard(player=player, kard=player.hand)
        board.draw(player=player)
