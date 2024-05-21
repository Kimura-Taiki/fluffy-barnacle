from pygame import Rect, Color, Surface, SRCALPHA, transform, image
from copy import deepcopy

from mod.screen import screen
from mod.func import rect_fill
from mod.font import MS_MINCHO_COL
from mod.kard import Kard
from ptc.square import Square
from ptc.player import Player
from ptc.element import Element

class PlayerSquare():
    def __init__(self, player: Player, rect: Rect) -> None:
        self.player = player
        self.rect = self._rect(rect=rect)
        self.img = self._img()

    def get_hover(self) -> Element | None:
        return None

    def draw(self) -> None:
        screen.blit(source=self.img, dest=self.rect)
        ...
        # rect_fill(color=self.translucent_color, rect=self.rect)
        # screen.blit(source=MS_MINCHO_COL(self.player.name, 24, "black"), dest=self.rect)
        # for i, kard in enumerate(self.player.log):
        #     dd

    @property
    def translucent_color(self) -> Color:
        color = deepcopy(self.player.color)
        color.a = int(color.a/2)
        return color

    def _rect(self, rect: Rect) -> Rect:
        w, h = (420*rect.h/288, rect.h) if rect.w*288 > rect.h*420 else (rect.w, 288*rect.w/420)
        return Rect(rect.left+(rect.w-w)/2, rect.top+(rect.h-h)/2, w, h)

    def _img(self) -> Surface:
        img = Surface(size=(420, 288), flags=SRCALPHA)
        rect_fill(color=self.translucent_color, rect=Rect(0, 0, 420, 288), surface=img)
        img.blit(source=MS_MINCHO_COL(self.player.name, 24, "black"), dest=(0, 0))
        for i, kard in enumerate(self.player.log):
            img.blit(
                source=transform.rotozoom(
                    surface=image.load(f"ll/pic/{kard.png_file}").convert_alpha(),
                    angle=0.0, scale=0.4),
                dest=(10+i*80, 70))
        return transform.rotozoom(surface=img, angle=0.0, scale=self.rect.w/420)