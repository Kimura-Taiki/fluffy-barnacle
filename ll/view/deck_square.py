from pygame import Rect, Color, Surface, SRCALPHA, transform

from any.pictures import IMG_BACK, IMG_REST, IMG_NUM
from any.func import rect_fill, ratio_rect, translucented_color
from any.screen import screen
from model.kard import Kard
from ptc.element import Element

from ptc.square import Square
class DeckSquare():
    _RATIO = (360, 495)

    def __init__(self, deck: list[Kard], rect: Rect) -> None:
        self.deck = deck
        self.rect = ratio_rect(rect=rect, ratio=self._RATIO)
        self.count_log = self.count
        self.img = self._img()
        self.img_back = transform.rotozoom(surface=IMG_BACK, angle=0.0, scale=self.rect.w/self._RATIO[0])

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
        img.blit(source=IMG_BACK, dest=(10, 10))
        img.blit(source=IMG_REST, dest=(90, 20))
        img.blit(source=IMG_NUM, dest=(210, 20), area=Rect(self.count%10*60, self.count//10*60, 60, 60))
        return transform.rotozoom(surface=img, angle=0.0, scale=self.rect.w/self._RATIO[0])

    @property
    def count(self) -> int:
        return len(self.deck)
