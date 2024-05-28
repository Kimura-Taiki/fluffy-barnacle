from pygame import Rect, Surface, SRCALPHA, transform

from any.screen import screen
from any.func import rect_fill, ratio_rect, translucented_color, cursor_in_rect
from any.font import MS_MINCHO_COL
from model.kard import Kard
from model.player import Player, OBSERVER
from ptc.bridge import Bridge
from ptc.element import Element

from ptc.square import Square
class HandSquare():
    _RATIO = (400, 288)
    _LOG_RATIO = (136, 190)

    def __init__(self, player_kard: Kard, draw_kard: Kard, rect: Rect, bridge: Bridge) -> None:
        self.player_kard = Kard
        self.draw_kard = Kard
        self.rect = ratio_rect(rect=rect, ratio=self._RATIO)
        self.bridge = bridge
        print(self.rect)

    def get_hover(self) -> Element | None:
        return None

    def draw(self) -> None:
        rect_fill(color=translucented_color("white"), rect=self.rect)
        # screen.fill(color=translucented_color("white"), rect=self.rect)
        # if self.player != self._now_player:
        #     self.player = self._now_player
        #     self.img = self._img()
        # screen.blit(source=self.img, dest=self.rect)
        # for log_square in self.log_squares:
        #     log_square.draw()
