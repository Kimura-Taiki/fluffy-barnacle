from pygame import Rect, Surface, SRCALPHA, transform, Vector2 as V2

from any.screen import screen
from any.font import MS_MINCHO_COL
from any.func import rect_fill, ratio_rect, translucented_color, cursor_in_rect
from any.pictures import IMG_BACK
from model.kard import Kard
from model.player import Player, OBSERVER
from ptc.bridge import Bridge
from ptc.element import Element

from ptc.square import Square
class HandSquare():
    _RATIO = (480, 432)
    _LOG_RATIO = (136, 190)

    def __init__(self, player_kard: Kard, draw_kard: Kard, rect: Rect, bridge: Bridge) -> None:
        self.player_kard = Kard
        self.draw_kard = Kard
        self.rect = ratio_rect(rect=rect, ratio=self._RATIO)
        self.bridge = bridge
        self.img = self._img()

    def get_hover(self) -> Element | None:
        return None

    def draw(self) -> None:
        screen.blit(source=self.img, dest=self.rect)

    def _img(self) -> Surface:
        img = Surface(size=self._RATIO, flags=SRCALPHA)
        rect_fill(color=translucented_color("white"), rect=Rect((0, 0), self._RATIO), surface=img)
        img_left = transform.rotozoom(surface=IMG_BACK, angle=5.0, scale=0.8)
        img_right = transform.rotozoom(surface=IMG_BACK, angle=-5.0, scale=0.8)
        img.blit(
            source=img_left,
            dest=V2(self._RATIO)/2-V2(img_left.get_size())/2-(80, 0)
        )
        img.blit(
            source=img_right,
            dest=V2(self._RATIO)/2-V2(img_left.get_size())/2+(80, 0)
        )
        return transform.rotozoom(surface=img, angle=0.0, scale=self.rect.w/self._RATIO[0])
