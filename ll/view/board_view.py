from pygame import Rect, Vector2 as V2
from typing import Callable

from any.screen import screen, WX, WY
from any.pictures import IMG_BG
from ctrl.draw_kards import DrawKardsController
from model.board import Board
from model.player import Player
from view.player_square import PlayerSquare
from view.deck_square import DeckSquare
from ptc.element import Element
from ptc.square import Square
from ptc.bridge import Bridge

_H = WY*2/5
_D = WX*3/16

from ptc.view import View
class BoardView():
    def __init__(self, subject: Player, bridge: Bridge) -> None:
        self.subject = subject
        self.bridge = bridge
        self.deck_square = self._deck_square()
        self.subject_square = self._subject_square()
        self.opponents_squares = self._opponents_squares(opponents=self.board.players, ds=self.deck_square)
        self.squares: list[Square] = [
            square for square in (self.deck_square, self.subject_square, *self.opponents_squares)
            if square is not None
        ]

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

    def draw_kard_action(self, player: Player, suffix: Callable[[], None] = lambda:None) -> Callable[[], None]:
        if (ps := self._player_square(player=player)):
            return self._draw_kard_ps_ds_func(
                ps=ps,
                ds=self.deck_square,
                suffix=suffix
            )
        else:
            raise ValueError(
                f"該当プレイヤーはいません\nplayer.name = {player.name}"+
                f"\nBoardView.board.player.names = {[player.name for player in self.board.players]}")

    def _deck_square(self) -> DeckSquare:
        return DeckSquare(deck=self.board.deck, rect=Rect(0, WY-_H, _D, _H))
    
    def _subject_square(self) -> PlayerSquare | None:
        return PlayerSquare(
            player=self.subject, rect=Rect(_D, WY-_H, WX/4, _H), bridge=self.bridge,
            ) if self.subject in self.board.players else None

    def _opponents_squares(self, opponents: list[Player], ds: DeckSquare) -> list[PlayerSquare]:
        w = WX/len(opponents)
        pss = [PlayerSquare(
            player=player,
            rect=Rect(w*i, 0, w, _H),
            bridge=self.bridge,)
            for i, player in enumerate(opponents)]
        for ps in pss:
            ps.mousedown = self._draw_kard_ps_ds_func(ps=ps, ds=ds)
        return pss

    def _draw_kard_ps_ds_func(
            self, ps: PlayerSquare, ds: DeckSquare, suffix: Callable[[], None]=lambda:None
    ) -> Callable[[], None]:
        return DrawKardsController(
            bridge=self.bridge,
            img_back=ds.img_back,
            from_v2=V2(ds.rect.center),
            to_v2=V2(ps.rect.center),
            player=ps.player,
            suffix=suffix
        ).action

    def _player_square(self, player: Player) -> PlayerSquare | None:
        return next((
            square for square in self.squares if\
            isinstance(square, PlayerSquare) and
            square.player.name == player.name), None)

    @property
    def board(self) -> Board:
        return self.bridge.board
