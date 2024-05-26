from pygame import Vector2 as V2

from ptc.listener import Listener
from view.deck_square import DeckSquare
from view.player_square import PlayerSquare
from view.draw_view import DrawView

from ptc.controller import Controller
class DrawKardsController():
    def __init__(self, listener: Listener, deck_square: DeckSquare, player_square: PlayerSquare) -> None:
        self.listener = listener
        self.deck_square = deck_square
        self.player_square = player_square

    def action(self) -> None:
        self._old_view = self.listener.view
        self.listener.view = DrawView(
            view=self._old_view,
            img_back=self.deck_square.img_back,
            from_v2=V2(self.deck_square.rect.center),
            to_v2=V2(self.player_square.rect.center),
            callback=self.callback
        )

    def callback(self) -> None:
        deck = self.listener.board.deck
        draw_kard = deck.pop(0)
        self.listener.board._replace(deck=deck, draw_kard=draw_kard)
        self.listener.view = self._old_view
