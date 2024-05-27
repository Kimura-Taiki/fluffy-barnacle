from pygame import Surface, Vector2 as V2
from typing import Callable

from model.player import Player
from model.kard import EMPTY_KARD
from ptc.bridge import Bridge
from view.draw_view import DrawView

from ptc.controller import Controller
class DrawKardsController():
    def __init__(
            self, bridge: Bridge, img_back: Surface, from_v2: V2, to_v2: V2, player: Player, suffix: Callable[[], None]
    ) -> None:
        self.bridge = bridge
        self.img_back = img_back
        self.from_v2 = from_v2
        self.to_v2 = to_v2
        self.player = player
        self.suffix = suffix

    def action(self) -> None:
        self._old_view = self.bridge.view
        self.bridge.view = DrawView(
            view=self._old_view,
            img_back=self.img_back,
            from_v2=self.from_v2,
            to_v2=self.to_v2,
            callback=self._default_callback
        )

    def _default_callback(self) -> None:
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
