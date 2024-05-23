from pygame import Rect, Color, Surface, SRCALPHA, transform, image
from copy import deepcopy

from any.screen import screen
from any.func import rect_fill, ratio_rect, translucented_color, pass_func, cursor_in_rect
from any.font import MS_MINCHO_COL
from model.kard import Kard
from view.log_square import LogSquare
from nf.exit import NfExit
from ptc.square import Square
from ptc.player import Player
from ptc.element import Element
from ptc.listener import Listener

class PlayerSquare():
    _RATIO = (320, 288)
    _LOG_RATIO = (136, 190)

    def __init__(self, player: Player, rect: Rect, listener: Listener) -> None:
        self.player = player
        self.rect = ratio_rect(rect=rect, ratio=self._RATIO)
        self.listener = listener
        self.img = self._img()
        self.log_squares = [LogSquare(
            kard=kard,
            rect=Rect((10+i*80, 70), self._LOG_RATIO),
            canvas=self.img
        ) for i, kard in enumerate(self.player.log)]
        self.draw = self._draw
        self.hover = lambda :None
        self.mousedown = self._mousedown
        self.active = lambda :None
        self.mouseup = lambda :None
        self.drag = lambda :None
        self.dragend = lambda :None

    def get_hover(self) -> Element | None:
        return self if cursor_in_rect(rect=self.rect) else None

    def _draw(self) -> None:
        screen.blit(source=self.img, dest=self.rect)
        for log_square in self.log_squares:
            log_square.draw()

    def _mousedown(self) -> None:
        # print(f"{self.player.name}をクリックしたよ")
        self.listener.listen(nf=NfExit())

    def _img(self) -> Surface:
        img = Surface(size=self._RATIO, flags=SRCALPHA)
        rect_fill(color=translucented_color(self.player.color), rect=Rect((0, 0), self._RATIO), surface=img)
        img.blit(source=MS_MINCHO_COL(f"{self.player.name} ({self.player.hand.name})", 24, "black"), dest=(0, 0))
        return transform.rotozoom(surface=img, angle=0.0, scale=self.rect.w/self._RATIO[0])
