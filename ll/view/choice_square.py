from pygame import Rect, Surface, SRCALPHA, transform, Vector2 as V2

from any.screen import screen
from any.func import rect_fill, ratio_rect, translucented_color, lcgs
from model.kard import Kard
from view.hand_square import HandSquare
from ptc.bridge import Bridge
from model.ui_element import UIElement

from ptc.square import Square
class ChoiceSquare():
    _RATIO = (480, 432)

    def __init__(self, rect: Rect, bridge: Bridge) -> None:
        self.rect = ratio_rect(rect=rect, ratio=self._RATIO)
        self.bridge = bridge
        self.old_hash = -1
        self.img = self._img()
        self.hqs = self._hqs()

    def get_hover(self) -> UIElement | None:
        if not self._has_two_hands:
            return None
        for square in self.hqs[::-1]:
            if element := square.get_hover():
                return element
        return None

    def draw(self) -> None:
        if not self._has_two_hands:
            return
        if self.old_hash != self._view_hash:
            self.old_hash = self._view_hash
            self.img = self._img()
            self.hqs = self._hqs()
        screen.blit(source=self.img, dest=self.rect)
        for hq in self.hqs:
            hq.draw()

    def elapse(self) -> None:
        for hq in self.hqs:
            hq.elapse()

    def _img(self) -> Surface:
        img = Surface(size=self._RATIO, flags=SRCALPHA)
        rect_fill(color=translucented_color("white"), rect=Rect((0, 0), self._RATIO), surface=img)
        return transform.rotozoom(surface=img, angle=0.0, scale=self.rect.w/self._RATIO[0])
    
    def _hqs(self) -> list[HandSquare]:
        if not self._has_two_hands:
            return []
        base_scale = 0.8 * self.rect.w / self._RATIO[0]
        centers = [
            V2(self.rect.center) - V2(80, 0),
            V2(self.rect.center) + V2(80, 0)
        ]
        angles = [5.0, -5.0]
        return [
            HandSquare(
                kard=self._hands[i],
                angle=angles[i],
                scale=base_scale,
                center=centers[i],
                bridge=self.bridge,
                canvas=screen,
            ) for i in range(2)
        ]

    @property
    def _view_hash(self) -> int:
        hash = 2
        for hand in self._hands:
            hash = lcgs(hash, hand.view_hash, 3)
        return hash
    
    @property
    def _hands(self) -> list[Kard]:
        return self.bridge.board.turn_player.hands

    @property
    def _has_two_hands(self) -> bool:
        return len(self._hands) == 2
