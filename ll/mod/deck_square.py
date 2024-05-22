from pygame import Rect, Color, Surface, SRCALPHA, transform, image, Vector2 as V2
from copy import deepcopy

from mod.screen import screen
from mod.func import rect_fill, ratio_rect, translucented_color
from mod.font import MS_MINCHO_COL
from mod.kard import Kard
from mod.log_square import LogSquare
from ptc.square import Square
from ptc.player import Player
from ptc.element import Element

class DeckSquare():
    _RATIO = (360, 495)
    _IMG_BACK = image.load("ll/pic/back.png").convert_alpha()
    _IMG_REST = image.load("ll/pic/rest.png").convert_alpha()
    _IMG_NUM = image.load("ll/pic/num.png").convert_alpha()

    def __init__(self, deck: list[Kard], rect: Rect) -> None:
        self.deck = deck
        self.rect = ratio_rect(rect=rect, ratio=self._RATIO)
        self.count_log = self.count
        self.img = self._img()

    def get_hover(self) -> Element | None:
        return None

    def draw(self) -> None:
        if self.count_log != self.count:
            self.count_log = self.count
            self.img = self._img()
        screen.blit(source=self.img, dest=self.rect)

    def _img(self) -> Surface:
        img = Surface(size=self._RATIO, flags=SRCALPHA)
        rect_fill(color=translucented_color(Color("coral")), rect=Rect((0, 0), self._RATIO), surface=img)
        img.blit(source=self._IMG_BACK, dest=(10, 10))
        img.blit(source=self._IMG_REST, dest=(90, 20))
        img.blit(source=self._IMG_NUM, dest=(210, 20), area=Rect(self.count%10*60, self.count//10*60, 60, 60))
        return transform.rotozoom(surface=img, angle=0.0, scale=self.rect.w/self._RATIO[0])

    @property
    def count(self) -> int:
        return len(self.deck)

# class PlayerSquare():
#     # _RATIO = (420, 288)
#     _RATIO = (320, 288)
#     _LOG_RATIO = (136, 190)

#     def __init__(self, player: Player, rect: Rect) -> None:
#         self.player = player
#         self.rect = ratio_rect(rect=rect, ratio=self._RATIO)
#         self.img = self._img()
#         self.log_squares = [LogSquare(
#             kard=kard,
#             rect=Rect((10+i*80, 70), self._LOG_RATIO),
#             canvas=self.img
#         ) for i, kard in enumerate(self.player.log)]

#     def get_hover(self) -> Element | None:
#         return None

#     def draw(self) -> None:
#         screen.blit(source=self.img, dest=self.rect)
#         for log_square in self.log_squares:
#             log_square.draw()

#     @property
#     def translucent_color(self) -> Color:
#         color = deepcopy(self.player.color)
#         color.a = int(color.a/2)
#         return color

#     def _img(self) -> Surface:
#         img = Surface(size=self._RATIO, flags=SRCALPHA)
#         rect_fill(color=self.translucent_color, rect=Rect((0, 0), self._RATIO), surface=img)
#         img.blit(source=MS_MINCHO_COL(f"{self.player.name} ({self.player.hand.name})", 24, "black"), dest=(0, 0))
#         return transform.rotozoom(surface=img, angle=0.0, scale=self.rect.w/self._RATIO[0])
