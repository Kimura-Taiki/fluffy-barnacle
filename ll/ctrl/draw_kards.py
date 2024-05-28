from pygame import Vector2 as V2
from typing import Callable

from model.player import Player
from model.kard import EMPTY_KARD
from ptc.bridge import Bridge
from view.board_view import BoardView
from view.linear_view import LinearView
from view.player_square import PlayerSquare

from ptc.controller import Controller
class DrawKardsController():
    def __init__(
            self,
            bridge: Bridge,
            board_view: BoardView,
            player: Player,
            pq: PlayerSquare | None=None,
            suffix: Callable[..., None]=lambda : None,
        ) -> None:
        self.bridge = bridge
        self.board_view = board_view
        self.player = player
        self.suffix = suffix
        dq = board_view.deck_square
        self.img_back = dq.img_back
        self.from_v2 = V2(dq.rect.center)
        self.to_v2 = V2((pq if pq else self._player_square()).rect.center)

    def action(self) -> None:
        self._old_view = self.bridge.view
        self.bridge.view = LinearView(
            view=self._old_view,
            img_back=self.img_back,
            from_v2=self.from_v2,
            to_v2=self.to_v2,
            callback=self._callback
        )

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

    def _callback(self) -> None:
        deck = self.bridge.board.deck
        draw_kard = deck.pop(0)
        if self.player.hand == EMPTY_KARD:
            players=[player._replace(hand=draw_kard)
                        if player.name == self.player.name else player
                        for player in self.bridge.board.players]
            self.bridge.board = self.bridge.board._replace(
                deck=deck,
                players=players
            )
        else:
            self.bridge.board = self.bridge.board._replace(deck=deck, draw_kard=draw_kard)
        self.bridge.view = self._old_view
        self.suffix()
