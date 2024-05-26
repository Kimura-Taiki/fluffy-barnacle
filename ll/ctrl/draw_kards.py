from pygame import Vector2 as V2
from typing import Callable

from model.board import Board
# from ptc.listener import Listener
from ptc.view import View
from view.deck_square import DeckSquare
from view.player_square import PlayerSquare
from view.draw_view import DrawView

from ptc.controller import Controller
class DrawKardsController():
    # def __init__(self, listener: Listener, deck_square: DeckSquare, player_square: PlayerSquare) -> None:
    #     self.listener = listener
    #     self.view = self.listener.view
    #     print("DrawKardsController.listener", self.listener.__class__)
    def __init__(self, board: Board, view: View, deck_square: DeckSquare, player_square: PlayerSquare) -> None:
        self.board = board
        self.view = view
        print("DrawKardsController.board", self.board.__class__)
        print("DrawKardsController.view", self.view.__class__)
        self.deck_square = deck_square
        self.player_square = player_square

    def action(self) -> None:
        print("Action!", self)
        self.view = DrawView(
            view=self.view,
            img_back=self.deck_square.img_back,
            from_v2=V2(self.deck_square.rect.center),
            to_v2=V2(self.player_square.rect.center),
            callback=self.callback
        )

    def callback(self) -> None:
        self.view = self.view

    # def _action(self, deck_square: DeckSquare, player_square: PlayerSquare) -> Callable[[], None]:
    #     def func() -> None:
    #         self.listener.view = DrawView(
    #             view=self.listener.view,
    #             img_back=deck_square.img_back,
    #             from_v2=V2(deck_square.rect.center),
    #             to_v2=V2(player_square.rect.center),
    #             callback=self._callback
    #         )
    #     return func

    # def _callback(self) -> None:
    #     self.listener.view = self