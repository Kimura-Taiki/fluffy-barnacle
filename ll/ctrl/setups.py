from pygame import Vector2 as V2

from ctrl.draw_kards import DrawKardsController
from model.kard import EMPTY_KARD
from ptc.bridge import Bridge
from view.deck_square import DeckSquare
from view.player_square import PlayerSquare
from view.draw_view import DrawView

from ptc.controller import Controller
class SetupsController():
    # def __init__(self, bridge: Bridge, deck_square: DeckSquare, player_square: PlayerSquare) -> None:
    def __init__(self, bridge: Bridge) -> None:
        self.bridge = bridge
        # self.deck_square = deck_square
        # self.player_square = player_square

    def action(self) -> None:
        handless_player = next((player for player in self.bridge.board.players if player.hand == EMPTY_KARD), None)
        if handless_player:
            DrawKardsController(
                bridge=self.bridge,
                deck_square=self.deck_square
            )
        self.callback()

    def callback(self, player) -> None:
        handless_player = next((player for player in self.bridge.board.players if player.hand == EMPTY_KARD), None)
        if handless_player:
            DrawKardsController(
                bridge=self.bridge,
                deck_square=self.bridge.view.
            ).action()

    def action(self) -> None:
        self._old_view = self.bridge.view
        self.bridge.view = DrawView(
            view=self._old_view,
            img_back=self.deck_square.img_back,
            from_v2=V2(self.deck_square.rect.center),
            to_v2=V2(self.player_square.rect.center),
            callback=self.callback
        )

    def callback(self) -> None:
        deck = self.bridge.board.deck
        draw_kard = deck.pop(0)
        if self.player_square.player.hand == EMPTY_KARD:
            players=[player._replace(hand=draw_kard)
                        if player.name == self.player_square.player.name else player
                        for player in self.bridge.board.players]
            self.bridge.board = self.bridge.board._replace(
                deck=deck,
                players=players
            )
        else:
            self.bridge.board = self.bridge.board._replace(deck=deck, draw_kard=draw_kard)
        self.bridge.view = self._old_view
