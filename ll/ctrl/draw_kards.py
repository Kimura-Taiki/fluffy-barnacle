from pygame import Vector2 as V2
from typing import Callable

from model.player import Player
from ptc.bridge import Bridge
from ptc.view import View
from view.board_view import BoardView
from view.linear_view import LinearView
from view.player_square import PlayerSquare

from ptc.controller import Controller
class DrawKardsController():
    def __init__(
            self,
            bridge: Bridge,
            board_view: View,
            player: Player,
            pq: PlayerSquare | None=None,
            suffix: Callable[..., None]=lambda : None,
        ) -> None:
        self.bridge = bridge
        if not isinstance(board_view, BoardView):
            raise ValueError("DrawKardsController を起動する時はBoardViewでないと", board_view)
        self.board_view = board_view
        self.player = player
        self.suffix = suffix
        dq = board_view.deck_square
        self.img_back = dq.img_back
        self.from_v2 = V2(dq.rect.center)
        self.to_v2 = V2((pq if pq else self._player_square()).rect.center)

    def action(self) -> None:
        self._old_view = self.bridge.view
        liner_view = LinearView(
            view=self._old_view,
            img_back=self.img_back,
            from_v2=self.from_v2,
            to_v2=self.to_v2,
        )
        self.bridge.view = liner_view
        self.bridge.whileloop(cond=liner_view.in_progress)
        self.bridge.board.draw(player=self.player)
        self.bridge.view = self._old_view
        self.suffix()

    def _player_square(self) -> PlayerSquare:
        if ps := next((
            square for square in self.board_view.squares if
            isinstance(square, PlayerSquare) and
            square.player.name == self.player.name
        ), None):
            return ps
        else:
            raise ValueError(
                f"該当プレイヤーはいません\nplayer.name = {self.player.name}"
            )
