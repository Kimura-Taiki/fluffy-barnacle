from pygame import Rect, Surface, SRCALPHA, transform, Vector2 as V2

from any.screen import screen
from any.func import rect_fill, ratio_rect, translucented_color
from model.kard import Kard, EMPTY_KARD
from view.hand_square import HandSquare
from ptc.bridge import Bridge
from model.ui_element import UIElement

from ptc.square import Square
class ChoiceSquare():
    _RATIO = (480, 432)

    def __init__(self, rect: Rect, bridge: Bridge) -> None:
        self.rect = ratio_rect(rect=rect, ratio=self._RATIO)
        self.bridge = bridge
        self.hands = self._now_hands
        self.img = self._img()
        self.hqs = self._hqs()

    def get_hover(self) -> UIElement | None:
        if self._is_negative:
            return None
        for square in self.hqs[::-1]:
            if element := square.get_hover():
                return element
        return None

    def draw(self) -> None:
        if self._is_negative:
            return
        if self.hands != self._now_hands:
            self.hands = self._now_hands
            self.img = self._img()
            self.hqs = self._hqs()
        screen.blit(source=self.img, dest=self.rect)
        for hq in self.hqs:
            hq.draw()

    def _img(self) -> Surface:
        img = Surface(size=self._RATIO, flags=SRCALPHA)
        rect_fill(color=translucented_color("white"), rect=Rect((0, 0), self._RATIO), surface=img)
        return transform.rotozoom(surface=img, angle=0.0, scale=self.rect.w/self._RATIO[0])
    
    def _hqs(self) -> list[HandSquare]:
        return [] if self._is_negative else [
            HandSquare(
                kard=self.hands[0],
                angle=5.0,
                scale=0.8*self.rect.w/self._RATIO[0],
                center=V2(self.rect.center)-V2(80, 0),
                bridge=self.bridge,
                canvas=screen
            ),
            HandSquare(
                kard=self.hands[1],
                angle=-5.0,
                scale=0.8*self.rect.w/self._RATIO[0],
                center=V2(self.rect.center)+V2(80, 0),
                bridge=self.bridge,
                canvas=screen
            ),
        ]
    
    @property
    def _is_negative(self) -> bool:
        return EMPTY_KARD in self._now_hands

    @property
    def _now_hands(self) -> list[Kard]:
        return [self.bridge.board.draw_kard, self.bridge.board.turn_player.hand]