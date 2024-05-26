from pygame import Rect, Vector2 as V2
from typing import Callable

from any.screen import screen, WX, WY
from any.pictures import IMG_BG
from model.board import Board
from model.player import Player
from view.player_square import PlayerSquare
from view.deck_square import DeckSquare
from view.draw_view import DrawView
from ptc.element import Element
from ptc.square import Square
from ptc.listener import Listener

_H = WY*2/5
_D = WX*3/16

from ptc.view import View
class BoardView():
    def __init__(self, board: Board, subject: Player, listener: Listener) -> None:
        self.board = board
        self.subject = subject
        self.listener = listener
        self.squares = self._squares()

    def rearrange(self) -> None:
        ...

    def get_hover(self) -> Element | None:
        for square in self.squares:
            if element := square.get_hover():
                return element
        return None

    def draw(self) -> None:
        screen.blit(source=IMG_BG, dest=[0, 0])
        for square in self.squares:
            square.draw()
        # if hover := self.get_hover():
        #     screen.fill(color=(255, 0, 0), rect=((hover.dest)-(10, 10), (20, 20)))

    def elapse(self) -> None:
        ...

    def _squares(self) -> list[Square]:
        opponents = [player for player in self.board.players if player != self.subject]
        ds = DeckSquare(deck=self.board.deck, rect=Rect(0, WY-_H, _D, _H))
        deck_square: list[Square] = [ds]
        opponents_squares = self._opponents_squares(opponents=opponents, ds=ds)
        subject_square: list[Square] = [
            PlayerSquare(player=self.subject, rect=Rect(_D, WY-_H, WX/4, _H), listener=self.listener,)
            ] if self.subject in self.board.players else []
        return opponents_squares+subject_square+deck_square

    def _opponents_squares(self, opponents: list[Player], ds: DeckSquare) -> list[Square]:
        w = WX/len(opponents)
        pss = [PlayerSquare(
            player=player,
            rect=Rect(w*i, 0, w, _H),
            listener=self.listener,)
            for i, player in enumerate(opponents)]
        for ps in pss:
            ps.mousedown = self._mousedown(
                deck_square=ds,
                player_square=ps)
        li: list[Square] = [square for square in pss]
        return li

    def _mousedown(self, deck_square: DeckSquare, player_square: PlayerSquare) -> Callable[[], None]:
        def func() -> None:
            self.listener.view = DrawView(
                view=self.listener.view,
                img_back=deck_square.img_back,
                from_v2=V2(deck_square.rect.center),
                to_v2=V2(player_square.rect.center),
                callback=self._callback
            )
        return func

    def _callback(self) -> None:
        raise EOFError("ヨシ！")
