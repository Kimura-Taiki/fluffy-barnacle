from pygame import Rect, Surface, SRCALPHA, transform

from any.screen import screen
from any.func import rect_fill, ratio_rect, translucented_color, cursor_in_rect
from any.font import MS_MINCHO_COL
from model.player import Player, OBSERVER
from model.ui_element import UIElement
from view.log_square import LogSquare
from ptc.bridge import Bridge

from ptc.square import Square
class PlayerSquare():
    _RATIO = (320, 288)
    _LOG_RATIO = (136, 190)

    def __init__(self, player: Player, rect: Rect, bridge: Bridge) -> None:
        self.player = player
        self.rect = ratio_rect(rect=rect, ratio=self._RATIO)
        self.bridge = bridge
        self.img = self._img()
        self.log_squares = [LogSquare(
            kard=kard,
            rect=Rect((10+i*80, 70), self._LOG_RATIO),
            canvas=self.img
        ) for i, kard in enumerate(self.player.log)]
        self.ui_element = UIElement()

    def get_hover(self) -> UIElement | None:
        return self.ui_element if cursor_in_rect(rect=self.rect) else None

    def draw(self) -> None:
        if self.player != self._now_player:
            self.player = self._now_player
            self.img = self._img()
        screen.blit(source=self.img, dest=self.rect)
        for log_square in self.log_squares:
            log_square.draw()

    def _img(self) -> Surface:
        img = Surface(size=self._RATIO, flags=SRCALPHA)
        hand_name = "(empty)" if len(self.player.hands) == 0 else self.player.hands[0].name
        rect_fill(color=translucented_color(self.player.color), rect=Rect((0, 0), self._RATIO), surface=img)
        img.blit(source=MS_MINCHO_COL(f"{self.player.name} ({hand_name})", 24, "black"), dest=(0, 0))
        return transform.rotozoom(surface=img, angle=0.0, scale=self.rect.w/self._RATIO[0])

    @property
    def _now_player(self) -> Player:
        return next((player for player in self.bridge.board.players if player.name == self.player.name), OBSERVER)
